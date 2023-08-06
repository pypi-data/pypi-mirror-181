from scipy import ndimage
from anntonia.visualizers.components import NodeVisualization
from anntonia.visualizers.data_transformation import *
from anntonia.server.state import LayerType
import anntonia.globals as globals


def ComputeNodeValuesFromPrevLayerWithActivation(reader, weighted_layer_sizes, weighted_layer_num, layer_num,
                                                 prev_layer, layer_type):
    node_values = []
    weights = reader.GetWeights()
    bias = reader.GetBias()

    if layer_type == LayerType.CONVOLUTIONAL:
        filter_shape = np.array(weights[weighted_layer_num]).shape
        filter_size = int(np.sqrt(filter_shape[0]))
        previous_side_length = weighted_layer_sizes[weighted_layer_num][0] + filter_size - 1

        if prev_layer.layer_type == LayerType.FULLY_CONNECTED:
            previous_shape = (previous_side_length, previous_side_length, 1)
        else:
            previous_shape = (
                previous_side_length, previous_side_length, int(weighted_layer_sizes[weighted_layer_num - 1][-1]))

        activation_input = FilterValues(prev_layer.node_values, previous_shape, weights[weighted_layer_num],
                                        bias[weighted_layer_num])
        node_values = np.array(reader.ApplyActivationFunction(np.array(activation_input), layer_num)).tolist()

    else:
        if prev_layer.layer_type == LayerType.FULLY_CONNECTED:
            for node in range(np.prod(weighted_layer_sizes[weighted_layer_num])):
                weighted_sum = np.sum(prev_layer.node_values * np.array(weights[weighted_layer_num])[:, node])
                activation_input = weighted_sum + bias[weighted_layer_num][0][node].tolist()
                node_values.append(np.array(reader.ApplyActivationFunction(np.array(activation_input), layer_num)).tolist())

        else:
            num_in_channel = weighted_layer_sizes[weighted_layer_num - 1][-1]
            for node in range(np.prod(weighted_layer_sizes[weighted_layer_num])):
                weighted_sum = 0
                ws = int(len(weights[weighted_layer_num]) / num_in_channel)
                # This loop is necessary because of how the weights are ordered in this particular case of layer combinations.
                for channel in range(num_in_channel):
                    weighted_sum += np.sum(prev_layer.node_values[channel * ws:(channel + 1) * ws] *
                                           np.array(weights[weighted_layer_num])[channel:len(weights[
                                                                                                 weighted_layer_num]) - num_in_channel + channel + 1:num_in_channel,
                                           node])

                activation_input = weighted_sum + bias[weighted_layer_num][0][node].tolist()
                node_values.append(np.array(reader.ApplyActivationFunction(np.array(activation_input), layer_num)).tolist())
    return node_values


def ComputeNodeValuesFromPrevLayer(reader, weighted_layer_sizes, weighted_layer_num, prev_layer, layer_type):
    node_values = []
    weights = reader.GetWeights()
    bias = reader.GetBias()

    if layer_type == LayerType.CONVOLUTIONAL:
        filter_shape = np.array(weights[weighted_layer_num]).shape
        filter_size = int(np.sqrt(filter_shape[0]))
        previous_side_length = weighted_layer_sizes[weighted_layer_num][0] + filter_size - 1

        if prev_layer.layer_type == LayerType.FULLY_CONNECTED:
            previous_shape = (previous_side_length, previous_side_length, 1)
        else:
            previous_shape = (
                previous_side_length, previous_side_length, int(weighted_layer_sizes[weighted_layer_num - 1][-1]))

        node_values = FilterValues(prev_layer.node_values, previous_shape, weights[weighted_layer_num],
                                   bias[weighted_layer_num])

    else:
        if prev_layer.layer_type == LayerType.FULLY_CONNECTED:
            for node in range(np.prod(weighted_layer_sizes[weighted_layer_num])):
                weighted_sum = np.sum(prev_layer.node_values * np.array(weights[weighted_layer_num])[:, node])
                node_values.append(weighted_sum + bias[weighted_layer_num][0][node].tolist())

        else:
            num_in_channel = weighted_layer_sizes[weighted_layer_num - 1][-1]
            for node in range(np.prod(weighted_layer_sizes[weighted_layer_num])):
                weighted_sum = 0
                ws = int(len(weights[weighted_layer_num]) / num_in_channel)
                # This loop is necessary because of how the weights are ordered in this particular case of layer combinations.
                for channel in range(num_in_channel):
                    weighted_sum += np.sum(prev_layer.node_values[channel * ws:(channel + 1) * ws] *
                                           np.array(weights[weighted_layer_num])[channel:len(weights[
                                                                                                 weighted_layer_num]) - num_in_channel + channel + 1:num_in_channel,
                                           node])

                node_values.append(weighted_sum + bias[weighted_layer_num][0][node].tolist())
    return node_values


def ComputeNodeValuesFromBias(reader, weighted_layer_sizes, weighted_layer_num, layer_type):
    node_values = []

    if layer_type == LayerType.FULLY_CONNECTED:
        node_values.append(reader.GetBias()[weighted_layer_num][0].tolist())
        node_values = np.ndarray.flatten(np.array(node_values)).tolist()
    elif layer_type == LayerType.CONVOLUTIONAL:
        for value in reader.GetBias()[weighted_layer_num][0]:
            node_values.append(
                np.full((weighted_layer_sizes[weighted_layer_num][0], weighted_layer_sizes[weighted_layer_num][1]),
                        value).tolist())
        node_values = np.ndarray.flatten(np.array(node_values)).tolist()

    return node_values


def SetNodeValues(node_visualization, reader, weighted_layer_sizes, weighted_layer_num, layer_num, prev_layer,
                  layer_type):
    """Gets the values of the nodes in a layer, depending on that enum in node_visualization."""
    if layer_type == LayerType.POOLING:
        # currently expects the previous layer to be a weighted layer
        node_values = MaxPoolValues(prev_layer.node_values, weighted_layer_sizes[weighted_layer_num - 1],
                                    reader.GetPoolSize(layer_num), reader.GetStride(layer_num))

    elif node_visualization == NodeVisualization.PREV_WITH_ACTIVATION:
        return ComputeNodeValuesFromPrevLayerWithActivation(reader, weighted_layer_sizes, weighted_layer_num, layer_num,
                                                            prev_layer, layer_type)

    elif node_visualization == NodeVisualization.PREV_WITHOUT_ACTIVATION:
        return ComputeNodeValuesFromPrevLayer(reader, weighted_layer_sizes, weighted_layer_num, prev_layer, layer_type)

    elif node_visualization == NodeVisualization.BIAS:
        return ComputeNodeValuesFromBias(reader, weighted_layer_sizes, weighted_layer_num, layer_type)

    else:
        raise TypeError(f"Invalid node visualization given for layer {layer_num}.")
    return node_values


def InputAsNodeValues(propagation_sample):
    """Returns the input sample as node values."""
    node_values = []
    for row in range(len(propagation_sample[0])):
        for node in range(len(propagation_sample[0][row])):
            node_values.append(propagation_sample[0][row][node].tolist())
    return node_values


def MaxPoolValues(node_values, prev_layer_shape, window_size, strides):
    """Returns the maximum pooled node_values"""
    values = []
    for i in range(prev_layer_shape[-1]):
        values.append(np.reshape(node_values[i*np.prod(prev_layer_shape[:2]):(i+1)*np.prod(prev_layer_shape[:2])], prev_layer_shape[:2]))
    values = np.array(values)
    w = window_size
    s = strides
    side_length0 = prev_layer_shape[0]
    side_length1 = prev_layer_shape[1]
    offset = [side_length0 - int((side_length0 + (s[0] - w[0])) / s[0])*s[0], side_length1 - int((side_length1 + (s[1] - w[1])) / s[1])*s[1]]
    pooled_values = np.zeros((int((side_length0-offset[0] - (w[0] - s[0]))/s[0]) * int((side_length1-offset[1] - (w[1] - s[1]))/s[1]) * prev_layer_shape[2]))
    for node in range(len(pooled_values)):
        win = values[int(node/int(len(pooled_values)/prev_layer_shape[2])),
                                        ((int((s[1]*node)/(side_length1-offset[1])) * s[0]) % (side_length0-offset[0])):((int((s[1]*node)/(side_length1-offset[1])) * s[0]) %(side_length0-offset[0])) + w[0],
                                            (s[1]*node)%(side_length1-offset[1]):((s[1]*node) % (side_length1-offset[1]))+w[1]]
        pooled_values[node] = np.max(win)

    return pooled_values.tolist()


def FilterValues(node_values, prev_layer_shape, filter, bias):
    '''Correlates the node_values of the previous layer with the given filter and returns the filtered values'''
    values = []
    num_in_channels = prev_layer_shape[-1]

    for i in range(num_in_channels):
        values.append(np.reshape(node_values[i * np.prod(prev_layer_shape[:2]):(i + 1) * np.prod(prev_layer_shape[:2])],
                                 prev_layer_shape[:2]))
    values = np.array(values)

    filter = SplitFilter(num_in_channels, filter)

    convolved_values = []

    for i in range(filter.shape[-1]):
        convolved_layer = ndimage.correlate(values[0], filter[:, :, 0, i])
        for j in range(1, filter.shape[-2]):
            convolved_layer += ndimage.correlate(values[j], filter[:, :, j, i])

        filter_halfsize = int(len(filter) / 2)
        convolved_layer = convolved_layer[filter_halfsize:-filter_halfsize, filter_halfsize:-filter_halfsize]
        convolved_layer += bias[0, i]
        convolved_layer = np.ndarray.flatten(convolved_layer).tolist()
        convolved_values.append(convolved_layer)

    return np.ndarray.flatten(np.array(convolved_values)).tolist()


def SplitFilter(num_in_channels, filter):
    '''Splits the filter weights as given by the GetWeights() function into an array of shape (side_length, side_length, num_in_channels, num_out_channels)'''
    filter_length = int(np.sqrt(len(filter)))
    num_out_channels = int(len(filter[0]) / num_in_channels)

    reshaped_filter = np.zeros((filter_length, filter_length, num_in_channels, num_out_channels))

    for j in range(num_out_channels):
        for i in range(num_in_channels):
            reshaped_filter[:, :, i, j] = np.reshape(filter[:, i + num_in_channels * j], (filter_length, filter_length),
                                                     order='F')
    return np.array(reshaped_filter)


def UpdateNodeValues(new_input):
    globals.currentServer.sync_state.layers[0].node_values = InputAsNodeValues(new_input)
    unweighted_layer = 0
    for i in range(1, globals.currentServer.sync_state.GetLayerCount()):
        globals.currentServer.sync_state.layers[i].node_values = SetNodeValues(
            NodeVisualization.PREV_WITH_ACTIVATION,
            globals.currentVisualizer.GetModel(),
            globals.currentVisualizer.GetModel().GetWeightedLayerSizes(),
            i - unweighted_layer - 1, i - 1, globals.currentServer.sync_state.layers[i - 1],
            globals.currentServer.sync_state.layers[i].layer_type)
        if globals.currentServer.sync_state.layers[i].layer_type == LayerType.POOLING:
            unweighted_layer += 1
    globals.currentServer.sync_state.UpdateNodeValues()
    globals.currentServer.UpdateState()
