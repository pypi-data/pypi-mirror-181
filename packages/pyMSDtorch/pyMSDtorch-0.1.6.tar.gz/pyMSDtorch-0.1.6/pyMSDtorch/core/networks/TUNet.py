import torch
import torch.nn as nn
from torch.autograd import Variable
from pyMSDtorch.core.networks import scale_up_down


def max_pool_size_result(Nin, stride=2, padding=1, dilation=1, kernel=3):
    """
    Determine what the size after a pooling operator is

    :param Nin: dimension of 1d array
    :param stride: stride
    :param padding: padding parameter
    :param dilation: dilation factor
    :param kernel: kernel size ; odd only please
    :return: the resulting array length
    """
    Nout = (Nin + 2 * padding - dilation * (kernel - 1) - 1) / stride + 1
    Nout = int(Nout)
    return Nout


def unet_sizing_chart(N, depth, stride, kernel, dilation=1):
    """
    Build a set of dictionairies that are useful to make sure that we can maps
    arrays back to the right sizes, for given strides and dilations.

    :param N: dimension of array
    :param depth: the total depth of the unet
    :param stride: the stride - we fix this for a single UNet
    :param kernel: the kernel size
    :param dilation: the dilation factor
    :return: a dictionairy with information

    The data associated with key "Sizes" provides images size per depth
    The data associated with key "Pool Setting" provides info needed to
    construct a MaxPool operator The data associated with key "convT
    Setting" provides info need to construct transposed convolutions such
    that the image of a the right size is constructed.

    """
    resulting_sizes = {}
    convT_settings = {}
    pool_settings = {}

    Nin = N
    for ii in range(depth):
        resulting_sizes[ii] = {}
        convT_settings[ii + 1] = {}
        pool_settings[ii] = {}
        Nout = max_pool_size_result(Nin,
                                    stride=stride,
                                    kernel=kernel,
                                    dilation=dilation,
                                    padding=(kernel - 1) / 2)
        pool_settings[ii][ii + 1] = {"padding": int((kernel - 1) / 2),
                                     "kernel": kernel,
                                     "dilation": dilation,
                                     "stride": stride}

        resulting_sizes[ii][ii + 1] = (Nin, Nout)

        padding, outp = scale_up_down.get_padding_convT(Nout, Nin,
                                                        dil=dilation,
                                                        stride=stride,
                                                        ker=kernel)
        Nup = scale_up_down.resulting_convT_size(Nout,
                                                 dil=dilation,
                                                 pad=padding,
                                                 stride=stride,
                                                 ker=kernel,
                                                 outp=outp)
        assert (Nin == Nup)
        convT_settings[ii + 1][ii] = {"padding": padding,
                                      "output_padding": outp,
                                      "kernel": kernel,
                                      "dilation": dilation,
                                      "stride": stride
                                      }

        Nin = Nout

    results = {"Sizes": resulting_sizes,
               "Pool_Settings": pool_settings,
               "convT_settings": convT_settings}
    return results


def build_up_operator(chart, from_depth, to_depth, in_channels,
                      out_channels, conv_kernel, key="convT_settings"):
    """
    Build an up sampling operator

    :param chart: An array of sizing charts (one for each dimension)
    :param from_depth: The sizing is done at this depth
    :param to_depth: and goes to this depth
    :param in_channels: number of input channels
    :param out_channels: number of output channels
    :param conv_kernel: the kernel we want to us
    :param key: a key we can use - default is fine
    :return: returns an operator
    """
    stride = []
    dilation = []
    kernel = []
    padding = []
    output_padding = []

    for ii in range(len(chart)):
        tmp = chart[ii][key][from_depth][to_depth]
        stride.append(tmp["stride"])
        dilation.append(tmp["dilation"])
        kernel.append(tmp["kernel"])
        padding.append(tmp["padding"])
        output_padding.append(chart[ii][key][from_depth][to_depth]["output_padding"])

    return conv_kernel(in_channels=in_channels,
                       out_channels=out_channels,
                       kernel_size=kernel,
                       stride=stride,
                       padding=padding,
                       output_padding=output_padding)


def build_down_operator(chart, from_depth, to_depth, conv_kernel, key="Pool_Settings"):
    """
    Build a down sampling operator

    :param chart: Array of sizing charts (one for each dimension)
    :param from_depth: we start at this depth
    :param to_depth: and go here
    :param conv_kernel: the kernel we want to us (MaxPool2D or MaxPool3D)
    :param key: a key we can use - default is fine
    :return: An operator with given specs
    """
    stride = []
    dilation = []
    kernel = []
    padding = []

    for ii in range(len(chart)):
        tmp = chart[ii][key][from_depth][to_depth]
        stride.append(tmp["stride"])
        dilation.append(tmp["dilation"])
        kernel.append(tmp["kernel"])
        padding.append(tmp["padding"])

    return conv_kernel(kernel_size=kernel,
                       stride=stride,
                       padding=padding)


class TUNet(nn.Module):
    """
    This implements a UNet with hopefully a bit better tunability
    on the number of parameters it uses.

    :param image_shape: image shape we use
    :param in_channels: input channels
    :param out_channels: output channels
    :param depth: the total depth
    :param base_channels: the first operator take in_channels->base_channels.
    :param growth_rate: The growth rate of number of channels per depth layer
    :param hidden_rate: How many 'inbetween' channels do we want? This is
                        relative to the feature channels at a given depth
    :param conv_kernel: The convolution kernel we want to us. Conv2D or Conv3D
    :param kernel_down: How do we steps down? MaxPool2D or MaxPool3D
    :param kernel_up: How do we step up? nn.ConvTranspose2d or
                      nn.ConvTranspose3d
    :param normalization: A normalization action
    :param activation: Activation function
    :param kernel_size: The size of the kernel we use
    :param stride: The stride we want to use.
    :param dilation: The dilation we want to use.

    """

    def __init__(self,
                 image_shape,
                 in_channels,
                 out_channels,
                 depth,
                 base_channels,
                 growth_rate=2,
                 hidden_rate=1,
                 conv_kernel=nn.Conv2d,
                 kernel_down=nn.MaxPool2d,
                 kernel_up=nn.ConvTranspose2d,
                 normalization=nn.BatchNorm2d,
                 activation=nn.ReLU(),
                 kernel_size=3,
                 stride=2,
                 dilation=1
                 ):
        """
        Construct a tuneable UNet

        :param image_shape: image shape we use
        :param in_channels: input channels
        :param out_channels: output channels
        :param depth: the total depth
        :param base_channels: the first operator take in_channels->base_channels.
        :param growth_rate: The growth rate of number of channels per depth layer
        :param hidden_rate: How many 'inbetween' channels do we want? This is
                            relative to the feature channels at a given depth
        :param conv_kernel: The convolution kernel we want to us. Conv2D or
                            Conv3D
        :param kernel_down: How do we steps down? MaxPool2D or MaxPool3D
        :param kernel_up: How do we step up? nn.ConvTranspose2d ore
                          nn.ConvTranspose3d
        :param normalization: A normalization action
        :param activation: Activation function
        :param kernel_size: The size of the kernel we use
        :param stride: The stride we want to use.
        :param dilation: The dilation we want to use.
        """
        super().__init__()
        # define the front and back of our network
        self.image_shape = image_shape
        self.in_channels = in_channels
        self.out_channels = out_channels

        # determine the overall arcvitecture
        self.depth = depth
        self.base_channels = base_channels
        self.growth_rate = growth_rate
        self.hidden_rate = hidden_rate

        # these are the convolution / pooling kernels
        self.conv_kernel = conv_kernel
        self.kernel_down = kernel_down
        self.kernel_up = kernel_up

        self.kernel_size = kernel_size
        self.stride = stride
        self.dilation = dilation

        # normalization and activation functions
        if normalization is not None:
            self.normalization = normalization
        else:
            self.normalization = None
        # print(activation)
        if activation is not None:
            self.activation = activation
        else:
            self.activation = nn.Identity()
        self.return_final_layer_ = False

        # we now need to get the sizing charts sorted
        self.sizing_chart = []
        for N in self.image_shape:
            self.sizing_chart.append(unet_sizing_chart(N=N,
                                                       depth=self.depth,
                                                       stride=self.stride,
                                                       kernel=self.kernel_size,
                                                       dilation=self.dilation))

        # setup the layers and partial / outputs
        self.encoder_layer_channels_in = {}
        self.encoder_layer_channels_out = {}
        self.encoder_layer_channels_middle = {}

        self.decoder_layer_channels_in = {}
        self.decoder_layer_channels_out = {}
        self.decoder_layer_channels_middle = {}

        self.partials_encoder = {}

        self.encoders = {}
        self.decoders = {}
        self.step_down = {}
        self.step_up = {}

        # first pass
        self.encoder_layer_channels_in[0] = self.in_channels
        self.decoder_layer_channels_out[0] = self.base_channels

        for ii in range(self.depth):

            # Match interlayer channels for stepping down
            if ii > 0:
                self.encoder_layer_channels_in[ii] = self.encoder_layer_channels_out[ii - 1]
            else:
                self.encoder_layer_channels_middle[ii] = int(self.base_channels)

            # Set base channels in first layer
            if ii == 0:
                self.encoder_layer_channels_middle[ii] = int(self.base_channels)
            else:
                self.encoder_layer_channels_middle[ii] = int(self.encoder_layer_channels_in[ii] * (self.growth_rate))

            # Apply hidden rate for growth within layers
            self.encoder_layer_channels_out[ii] = int(self.encoder_layer_channels_middle[ii] * self.hidden_rate)

            # Decoder layers match Encoder channels
            self.decoder_layer_channels_in[ii] = self.encoder_layer_channels_out[ii]
            self.decoder_layer_channels_middle[ii] = self.encoder_layer_channels_middle[ii]
            self.decoder_layer_channels_out[ii] = self.encoder_layer_channels_in[ii]

            self.partials_encoder[ii] = None

        # Correct final decoder layer
        self.decoder_layer_channels_out[0] = self.encoder_layer_channels_middle[0]

        # Correct first decoder layer
        self.decoder_layer_channels_in[depth-2] = self.encoder_layer_channels_in[depth-1]

        # Second pass, add in the skip connections
        for ii in range(depth - 1):
            self.decoder_layer_channels_in[ii] += self.encoder_layer_channels_out[ii]

        for ii in range(depth):

            if ii < (depth - 1):

                # Build encoder/decoder layers
                self.encoders[ii] = "Encode_%i" % ii
                tmp = self.build_unet_layer(self.encoder_layer_channels_in[ii],
                                            self.encoder_layer_channels_middle[ii],
                                            self.encoder_layer_channels_out[ii])
                self.add_module(self.encoders[ii], tmp)

                self.decoders[ii] = "Decode_%i" % ii

                if ii == 0:
                    tmp = self.build_output_layer(
                        self.decoder_layer_channels_in[ii],
                        self.decoder_layer_channels_middle[ii],
                        self.decoder_layer_channels_out[ii],
                        self.out_channels)
                    self.add_module(self.decoders[ii], tmp)
                else:
                    tmp = self.build_unet_layer(self.decoder_layer_channels_in[ii],
                                                self.decoder_layer_channels_middle[ii],
                                                self.decoder_layer_channels_out[ii])
                    self.add_module(self.decoders[ii], tmp)
            else:
                self.encoders[ii] = "Final_layer_%i" % ii
                tmp = self.build_unet_layer(self.encoder_layer_channels_in[ii],
                                            self.encoder_layer_channels_middle[
                                                ii],
                                            self.encoder_layer_channels_out[
                                                ii])
                self.add_module(self.encoders[ii], tmp)

            # Build stepping operations
            if ii < self.depth - 1:
                # we step down like this
                self.step_down[ii] = "Step Down %i" % ii
                tmp = build_down_operator(chart=self.sizing_chart,
                                          from_depth=ii,
                                          to_depth=ii + 1,
                                          conv_kernel=self.kernel_down,
                                          key="Pool_Settings")
                self.add_module(self.step_down[ii], tmp)
            if (ii >= 0) and (ii < depth - 1):
                # we step up like this

                self.step_up[ii] = "Step Up %i" % ii
                if ii == (depth - 2):
                    tmp = build_up_operator(chart=self.sizing_chart,
                                            from_depth=ii + 1,
                                            to_depth=ii,
                                            in_channels=self.encoder_layer_channels_out[ii + 1],
                                            out_channels=self.encoder_layer_channels_out[ii],
                                            conv_kernel=self.kernel_up,
                                            key="convT_settings")
                else:
                    tmp = build_up_operator(chart=self.sizing_chart,
                                            from_depth=ii + 1,
                                            to_depth=ii,
                                            in_channels=self.decoder_layer_channels_out[ii + 1],
                                            out_channels=self.encoder_layer_channels_out[ii],
                                            conv_kernel=self.kernel_up,
                                            key="convT_settings")

                self.add_module(self.step_up[ii], tmp)


    def build_unet_layer(self, in_channels, in_between_channels, out_channels):
        """
        Build a sequence of convolutions with activations functions and
        normalization layers

        :param in_channels: input channels
        :param in_between_channels: the in between channels
        :param out_channels: the output channels
        :return:
        """

        if self.normalization is not None:
            operator = nn.Sequential(self.conv_kernel(in_channels,
                                                      in_between_channels,
                                                      kernel_size=self.kernel_size,
                                                      padding=int((self.kernel_size - 1) / 2)),
                                     self.normalization(in_between_channels),
                                     self.activation,
                                     self.conv_kernel(in_between_channels,
                                                      out_channels,
                                                      kernel_size=self.kernel_size,
                                                      padding=int((self.kernel_size - 1) / 2)),
                                     self.normalization(out_channels),
                                     self.activation
                                     )
        else:
            operator = nn.Sequential(self.conv_kernel(in_channels,
                                                      in_between_channels,
                                                      kernel_size=self.kernel_size,
                                                      padding=int((self.kernel_size - 1) / 2)),
                                     self.activation,
                                     self.conv_kernel(in_between_channels,
                                                      out_channels,
                                                      kernel_size=self.kernel_size,
                                                      padding=int((self.kernel_size - 1) / 2)),
                                     self.activation
                                     )

        return operator

    def build_output_layer(self, in_channels,
                           in_between_channels1,
                           in_between_channels2,
                           final_channels):
        """
        Build a sequence of convolutions with activations functions and
        normalization layers

        :param final_channels: The output channels
        :type final_channels: int
        :param in_channels: input channels
        :param in_between_channels1: the in between channels after first convolution
        :param in_between_channels2: the in between channels after second convolution
        "param final_channels: number of channels the network outputs
        :return:
        """
        if self.normalization is not None:
            operator = nn.Sequential(self.conv_kernel(in_channels,
                                                      in_between_channels1,
                                                      kernel_size=self.kernel_size,
                                                      padding=int((self.kernel_size - 1) / 2)),
                                     self.normalization(in_between_channels1),
                                     self.activation,
                                     self.conv_kernel(in_between_channels1,
                                                      in_between_channels2,
                                                      kernel_size=self.kernel_size,
                                                      padding=int((self.kernel_size - 1) / 2)),
                                     self.normalization(in_between_channels2),
                                     self.activation,
                                     self.conv_kernel(in_between_channels2,
                                                      final_channels,
                                                      kernel_size=1)
                                     )
        else:
            operator = nn.Sequential(self.conv_kernel(in_channels,
                                                      in_between_channels1,
                                                      kernel_size=self.kernel_size,
                                                      padding=int((self.kernel_size - 1) / 2)),
                                     self.activation,
                                     self.conv_kernel(in_between_channels1,
                                                      in_between_channels2,
                                                      kernel_size=self.kernel_size,
                                                      padding=int((self.kernel_size - 1) / 2)),
                                     self.activation,
                                     self.conv_kernel(in_between_channels2,
                                                      final_channels,
                                                      kernel_size=1)
                                     )
        return operator

    def forward(self, x):
        """
        Default forward operator.

        :param x: input tensor.
        :return: output of neural network
        """

        # first pass through the encoder
        for ii in range(self.depth - 1):
            # channel magic
            x_out = self._modules[self.encoders[ii]](x)

            # store this for decoder side processing
            self.partials_encoder[ii] = x_out

            # step down
            x = self._modules[self.step_down[ii]](x_out)
            # done


        # last convolution in bottom, no need to stash results
        x = self._modules[self.encoders[self.depth - 1]](x)


        for ii in range(self.depth - 2, 0, -1):
            x = self._modules[self.step_up[ii]](x)
            x = torch.cat((self.partials_encoder[ii], x), dim=1)
            x = self._modules[self.decoders[ii]](x)


        x = self._modules[self.step_up[0]](x)
        x = torch.cat((self.partials_encoder[0], x), dim=1)
        x_out = self._modules[self.decoders[0]](x)


        return x_out


def tst():
    a = 64
    b = 64
    obj = TUNet(image_shape=(a, b),
                in_channels=1,
                out_channels=1,
                depth=4,
                base_channels=32,
                growth_rate=1.2,
                hidden_rate=1.3,
                normalization=None
                # activation=None
                )

    from torchsummary import summary
    from pyMSDtorch.core import helpers
    device = helpers.get_device()
    obj.to(device)
    #summary(obj, (1, a, b))

    x = Variable(
        torch.rand(20, 1, a, b))
    x = x.cuda()

    from time import time
    starttime = time()

    times = []
    for j in range(11):
        start = time()

        x = obj(x)
        torch.cuda.empty_cache()

        end = time()
        elapsed = end - start
        times.append(elapsed)
    endtime = time()

    print('First run time: ', times[0])

    print('Avg of all others: ', sum(times[1:]) / (len(times) - 1))

    # print('Input shape: ', x.size())
    # print('Output size: ', y.size())
    return True


if __name__ == "__main__":
    assert tst()
