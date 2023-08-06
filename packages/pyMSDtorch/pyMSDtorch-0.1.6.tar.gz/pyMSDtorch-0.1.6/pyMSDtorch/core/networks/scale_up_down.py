"""
Some tools to compute padding and output_pad sizes.
"""


def resulting_conv_size(Hin, dil, pad, stride, ker):
    """
    Computes the resulting size of a tensor dimension given conv input parameters

    Parameters
    ----------
    Hin : input dimension
    dil : dilation
    pad : padding
    stride : stride
    ker : kernsel size

    Returns
    -------
    the size of the resulting tensor

    """
    N0 = (Hin + 2 * pad - dil * (ker - 1) - 1) / stride + 1
    return int(N0)


def resulting_convT_size(Hin, dil, pad, stride, ker, outp):
    """
    Computes the resulting size of a tensor dimension given convT input parameters

    Parameters
    ----------
    Hin : input dimension
    dil : dilation
    pad : padding
    stride : stride
    ker : kernel size
    outp : the outp parameter

    Returns
    -------
    the size of the resulting tensor
    """
    N0 = (Hin - 1) * stride - 2 * pad + dil * (ker - 1) + outp + 1
    return N0


def get_padding_convT(Nsmall, Nbig, dil, stride, ker):
    """
    Compute the padding and output padding values to make sure that
    you go from Nsmall to Nbig in a transposed conv setting.

    :param Nsmall: small array dimensions (start)
    :param Nbig: bigh arrayt dimension (end)
    :param dil: dilation
    :param stride: stride
    :param ker: kernel size
    :return: the padding and output_padding
    """
    tmp = -(Nbig - (Nsmall - 1) * stride - dil * (ker - 1) - 1)
    if tmp % 2 == 0:
        outp = 0
        padding = int(tmp / 2)
    else:
        outp = 1
        padding = int((tmp + 1) / 2)
    assert padding >= 0
    return padding, outp


def conv_padding(dil, kernel):
    """
    Do we need a function for this?
    :param dil: Dilation
    :param kernel: Stride
    :return: needed padding value
    """
    return int(dil * (kernel - 1) / 2)


def scaling_table(input_size, stride_base, min_power, max_power, kernel):
    """
    A generic scaling table for a variety of possible scale change options.
    :param input_size: input image size
    :param stride_base: the stride_base we want to use
    :param min_power: determines the minimum stride: stride = stride_base**min_power
    :param max_power: determines the maximum stride: stride = stride_base**min_power
    :param kernel: kernel size
    :return: A dict with various settings
    #TODO: DEBUG THIS for stride_base!=2
    """
    # first establish the output sizes with respect to the input these
    # operations are agnostic to dilation sizes as long as padding is chosen
    # properly
    _dil = 1
    _pad = conv_padding(_dil, kernel)

    # get sizes we need to address
    available_sizes = []
    powers = range(min_power, max_power + 1)
    stride_output_padding_dict = {}
    for power in powers:
        # if we scale the image down, we use conv
        if power <= 0:
            stride = stride_base ** (-power)
            out_size = resulting_conv_size(input_size, _dil,
                                           _pad, stride, kernel)
            available_sizes.append(out_size)
            stride_output_padding_dict[power] = {}

        # if we scale up we use conv_transpose
        if power > 0:
            stride = stride_base ** power
            out_size = stride * input_size
            available_sizes.append(out_size)
            stride_output_padding_dict[power] = {}

    # now we need to figure out how to go between different sizes

    for ii in range(len(powers)):
        for jj in range(len(powers)):
            size_A = available_sizes[ii]
            size_B = available_sizes[jj]
            power_A = int(powers[ii])
            power_B = int(powers[jj])
            delta_power = power_B - power_A

            # we have to scale up, so we use conv_transpose
            if delta_power > 0:
                stride = stride_base ** delta_power
                add_pad = size_B - resulting_convT_size(size_A, _dil, _pad,
                                                        stride, kernel, 0)
                stride_output_padding_dict[power_A][power_B] = (stride,
                                                                add_pad)

            else:
                stride = stride_base ** -delta_power
                stride_output_padding_dict[power_A][power_B] = (stride, None)

    return stride_output_padding_dict


if __name__ == "__main__":
    scaling_table(64, stride_base=2, min_power=-1, max_power=1, kernel=3)
