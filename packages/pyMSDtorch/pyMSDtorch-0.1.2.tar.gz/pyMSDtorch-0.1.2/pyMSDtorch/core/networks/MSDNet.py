import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from pyMSDtorch.core import helpers


class MixedScaleDenseLayer(nn.Module):
    """Object which builds a single 'layer' in our MSDNetwork"""

    def __init__(self, convolution, in_channels, dilations,
                 padding_mode, kernel_size=3):
        """
        :param convolution: one of nn.Conv2d or nn.Conv3d classes
        :param in_channels: number of channels in input data (1 if
                            grayscale, 3 if color); acts as the depth,
                            or third dimensional number, for all 2D
                            convolutions
        :param dilations: dilation sizes for each channel in current
                          layer
        :param padding_mode: padding mode chosen to fill boundary space
        :param kernel_size: the n by n size of filter mask (3 or 5
                            chosen almost universally for CNNs)
        """

        super(MixedScaleDenseLayer, self).__init__()

        self.out_channels = in_channels + len(dilations)

        for j, dilation in enumerate(dilations):
            dilated_kernel_size = (kernel_size - 1) * dilation + 1
            padding = dilated_kernel_size // 2
            self.add_module(f'conv_{j}', convolution(in_channels, 1,
                                                     kernel_size=kernel_size,
                                                     dilation=dilation,
                                                     padding=padding,
                                                     padding_mode=padding_mode
                                                     ))

    def forward(self, x):
        """
        Standard forward operator

        Parameters
        ----------
        x : input tensor

        Returns
        -------
        output tensor
        """
        return torch.cat((x,) + tuple(c(x) for c in self.children()), dim=1)


class MixedScaleDenseNetwork(nn.Sequential):
    """
    Defines Mixed Scale Dense Network based on topology (number of
    layers and channels per layer) and morphology (dilation sizes for
    each feature map). Input and output layer sizes are passed as
    input, including user-defined activation dropout rates and
    activation layers.

    :param int in_channels: number of channels in input data
    :param int out_channels: number of channels in output data
    :param num_layers: depth of network
    :type num_layers: int or None
    :param layer_width: width of each layer
    :type layer_width: int or None
    :param max_dilation: maximum dilation size the network will
                         cycle through
    :type max_dilation: int or None
    :param custom_MSDNet: n by m numnpy array whose dimensions
                          define the network topology (m number of
                          layers and n channels per layer) and
                          entries define the morphology (size of
                          dilated kernel at each channel)
    :type custom_MSDNet: List[int]
    :param int kernel_size: n by n size of filter mask (odd; 3 or 5
                            are best values)
    :param activation: instance of PyTorch activation class applied
                       to each layer. If passing a list of
                       multiple activation class instances, each
                       will be applied in the order given.
                       ex) activation=nn.ReLU()
                       ex) activation=nn.RReLU(lower=.1, upper=.9)
                       ex) activation=[nn.ReLU(), nn.Sigmoid()]
    :type activation: torch.nn class instance or list of torch.nn
                      class instances
    :param normalization: PyTorch normalization class applied to
                          each layer. Passed as class without
                          parentheses since we need a different
                          instance per layer
                          ex) normalization=nn.BatchNorm2d
    :type normalization: torch.nn class
    :param final_layer: instance of PyTorch activation class applied
                        after final layer. If passing a list of
                        multiple activation class instances, each
                        will be applied in the order given.
                          ex) normalization=nn.Sigmoid()
                          ex) normalization=nn.Softmax(dim=1)
    :param int kernel_size: the n by n size of filter mask applied
                            to all but final convolution (3 or 5
                            chosen almost universally for CNNs)
    :param dropout: 1 by 3 numpy.ndarray defining drop out rate for
                    [initial, hidden, final] layers. If none,
                    dropout is not used
    :type dropout: List[Union[int,float]]
    :param convolution: instance of PyTorch convolution class.
                        Accepted are nn.Conv1d, nn.Conv2d, and
                        nn.Conv3d.
    :type convolution: torch.nn class instance
    :param str padding_mode: padding mode to be used in convolution
                             to fill boundary space. Accepted input
                             are  'zeros', 'reflect', 'replicate' or
                             'circular'

    Instructions: User has two options for building network topology and
    morphology:
        1)  to generate a network based on number of layers, channels,
            and the number of dilations to cycle through, pass integers
            in for num_layers, layer_width, and max_dilation
            and leave custom_MSDNet = None
                ex) num_layers=5, layer_width=2, max_dilation=5
                    yields the network [1, 3, 5, 2, 4, 1
                                        2, 4, 1, 3, 5, 2]
        2)  to create a custom network with user-specified dilation
            sizes, network depth, and layer width, pass in:
                    a) num_layers = layer_width
                                  = max_dilation
                                  = None
                    b)  numpy array populated with desired
                        integer-valued dilations whose columns
                        correspond to network layers and number of rows
                        corresponds to number of channels per layer
    Referenece paper: A mixed-scale dense convolutional neural network for
                      image analysis
    Published: PNAS, Jan. 2018
    Link: http://www.pnas.org/content/early/2017/12/21/1715832114

    Note: Bias=True is Conv2d and Conv3d default
    """

    def __init__(self, in_channels,
                 out_channels,
                 num_layers=10,
                 layer_width=1,
                 max_dilation=10,
                 custom_MSDNet=None,
                 activation=None,
                 normalization=None,
                 final_layer=None,
                 kernel_size=3,
                 dropout=None,
                 convolution=nn.Conv2d,
                 padding_mode="zeros"):
        """
        Build an MSDNet given the spoecs listed below.

        :param int in_channels: number of channels in input data
        :param int out_channels: number of channels in output data
        :param num_layers: depth of network
        :type num_layers: int or None
        :param layer_width: width of each layer
        :type layer_width: int or None
        :param max_dilation: maximum dilation size the network will
                             cycle through
        :type max_dilation: int or None
        :param custom_MSDNet: n by m numnpy array whose dimensions
                              define the network topology (m number of
                              layers and n channels per layer) and
                              entries define the morphology (size of
                              dilated kernel at each channel)
        :type custom_MSDNet: List[int]
        :param int kernel_size: n by n size of filter mask (odd; 3 or 5
                                are best values)
        :param activation: instance of PyTorch activation class applied
                           to each layer. If passing a list of
                           multiple activation class instances, each
                           will be applied in the order given.
                           ex) activation=nn.ReLU()
                           ex) activation=nn.RReLU(lower=.1, upper=.9)
                           ex) activation=[nn.ReLU(), nn.Sigmoid()]
        :type activation: torch.nn class instance or list of torch.nn
                          class instances
        :param normalization: PyTorch normalization class applied to
                              each layer. Passed as class without
                              parentheses since we need a different
                              instance per layer
                              ex) normalization=nn.BatchNorm2d
        :type normalization: torch.nn class
        :param final_layer: instance of PyTorch activation class applied
                            after final layer. If passing a list of
                            multiple activation class instances, each
                            will be applied in the order given.
                              ex) normalization=nn.Sigmoid()
                              ex) normalization=nn.Softmax(dim=1)
        :param int kernel_size: the n by n size of filter mask applied
                                to all but final convolution (3 or 5
                                chosen almost universally for CNNs)
        :param dropout: 1 by 3 numpy.ndarray defining drop out rate for
                        [initial, hidden, final] layers. If none,
                        dropout is not used
        :type dropout: List[Union[int,float]]
        :param convolution: instance of PyTorch convolution class.
                            Accepted are nn.Conv1d, nn.Conv2d, and
                            nn.Conv3d.
        :type convolution: torch.nn class instance
        :param str padding_mode: padding mode to be used in convolution
                                 to fill boundary space. Accepted input
                                 are  'zeros', 'reflect', 'replicate' or
                                 'circular'
        """
        super(MixedScaleDenseNetwork, self).__init__()

        # nonzero padding results in an error when using 2d convolutions
        if convolution == nn.Conv3d:
            padding_mode = 'zeros'

        # Add dropout as activation layer
        if dropout is not None:
            self.add_module('initial dropout', nn.Dropout(p=dropout[0]))

        # Get number of channels feeding into first layer
        current_channels = in_channels

        # Retrieve number of layers if using a custom network
        if custom_MSDNet is not None:
            if custom_MSDNet.ndim == 1:

                num_rep = int(np.ceil(num_layers / len(custom_MSDNet)))
                custom_MSDNet = np.tile(custom_MSDNet, num_rep)
                custom_MSDNet = custom_MSDNet[0:num_layers]
                custom_MSDNet = custom_MSDNet.reshape(1,
                                                      custom_MSDNet.shape[0])
            else:
                num_layers = custom_MSDNet.shape[1]

        # Begin building layers using loop
        for i in range(num_layers):

            if custom_MSDNet is not None:
                dilations = custom_MSDNet[:, i]
            else:
                dilations = [((i * layer_width + j) % max_dilation) +
                             1 for j in range(layer_width)]

            layer = MixedScaleDenseLayer(convolution, current_channels,
                                         dilations,
                                         padding_mode,
                                         kernel_size)

            # Append convolutional layer and update number of channels
            self.add_module(f'layer_{i}', layer)
            current_channels = layer.out_channels

            # Add dropout to middle hidden layers before activation
            # if i == int(np.ceil(num_layers / 2)):
            if dropout is not None:
                # print('add dropout')
                self.add_module(f'dropout_{i}', nn.Dropout(p=dropout[1]))

            # Add activation and normalization after each block
            if activation is not None:
                try:
                    for j, single_activation in enumerate(activation):
                        self.add_module(f'activation_{i}_{j + 1}',
                                        single_activation)
                except TypeError:
                    self.add_module(f'activation_{i}', activation)

            # Add normalization after each block
            if normalization is not None:
                self.add_module(f'normalization_{i}', normalization(
                    current_channels))

        # Create final layer, add final activation, and apply dropout,
        if dropout is not None:
            self.add_module('final_dropout', nn.Dropout(p=dropout[2]))

        # Always add 2d convolution with kernel size 1
        self.add_module('final_convolution', convolution(
            current_channels, out_channels, kernel_size=1))

        # Add activation after final layer
        if final_layer is not None:
            self.add_module(f'final_activation', final_layer)


def tst(show_network=True):
    """
    Defines and test several Mixed Scale Dense Networks consisting of 2D
    convolutions, provides a printout of the network, and checks to make
    sure tensors pass through the network

    :param show_network: if True, print out each network
    """

    # Create a network with ReLU and BatchNorm activation functions
    network1 = MixedScaleDenseNetwork(in_channels=1,
                                      out_channels=1,
                                      num_layers=5,
                                      layer_width=2,
                                      max_dilation=10,
                                      activation=[nn.ReLU(inplace=True),
                                                  nn.Sigmoid()],
                                      normalization=nn.BatchNorm2d,
                                      final_layer=nn.Sigmoid(),
                                      dropout=[0, .2, 0]
                                      )

    print('\n### Basic network with ReLU ###')
    print('###############################')
    print('Number of learnable parameters:',
          helpers.count_parameters(network1))
    print('Number of layers:', helpers.count_conv2d(network1))
    if show_network is True:
        print(network1)

    # Create a custom network for 3-channel input/1-channel output
    network2 = MixedScaleDenseNetwork(in_channels=3,
                                      out_channels=1,
                                      num_layers=22,
                                      layer_width=None,
                                      max_dilation=None,
                                      dropout=[.1, .2, .3],
                                      custom_MSDNet=np.array([1, 2, 4, 8, 16])
                                      )

    print('\n### Custom network ####')
    print('#######################')
    print('Number of learnable parameters:',
          helpers.count_parameters(network2))
    print('Number of layers:', helpers.count_conv2d(network2))
    if show_network is True:
        print(network2)

    x = Variable(torch.rand(8, 3, 32, 32))
    y = network2(x)  # pass tensor through the network

    print('Dimensions of the input and output images')
    print('x: ', x.shape)
    print('y: ', y.shape)

    # Pass a stack of three dimensional images with color channel using
    # 3D convolutions
    network3 = MixedScaleDenseNetwork(in_channels=1,
                                      out_channels=1,
                                      num_layers=4,
                                      layer_width=1,
                                      max_dilation=10,
                                      activation=nn.ReLU(),
                                      normalization=nn.BatchNorm3d,
                                      dropout=[0, .2, .5],
                                      final_layer=nn.LogSoftmax(dim=1),
                                      convolution=nn.Conv3d
                                      )

    print('\n### Simple network using Conv3d ###')
    print('#######################################')
    print('Number of learnable parameters:',
          helpers.count_parameters(network3))
    print('Number of layers:', helpers.count_conv3d(network3))
    if show_network is True:
        print(network3)

    x = Variable(
        torch.rand(8, 1, 32, 32, 32))  # stack of 8 three-channel images
    y = network3(x)  # pass tensor through the network

    print('Dimensions of the input and output images')
    print('x: ', x.shape)
    print('y: ', y.shape)


if __name__ == "__main__":
    tst()
