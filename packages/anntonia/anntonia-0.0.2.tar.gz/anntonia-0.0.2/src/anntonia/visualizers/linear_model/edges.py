from anntonia.server.state import LayerType
from anntonia.visualizers.data_transformation import *
from anntonia.utils.relevance_propagation import LayerwiseRelevancePropagation
from anntonia.visualizers.linear_model.node_values import SplitFilter
from anntonia.visualizers.components import *


def ComputeActivationOutput(reader, propagation_image, propagation_image_label):
    """Computes the activation output for a given image and layer.
    Uses layerwise relevance propagation if an image label is given."""
    activation_output = reader.GetActivationOutputAllLayers(propagation_image)
    if propagation_image_label is not None:
        activation_output = LayerwiseRelevancePropagation(reader.GetWeights(), reader.GetBias(),
                                                          propagation_image_label, activation_output)

    return activation_output


def UseWeightsAsLinkValues(reader, layer_sizes, start_layer_num, weights, current_state, edge_representation):
    """Assigns the links of a layer the corresponding weights als values."""
    link_values = []
    weightless_layer = [l.layer_type == LayerType.POOLING for l in current_state.layers[:start_layer_num+1]].count(True)

    if isinstance(edge_representation, FilterEdgeRepresentation):
        num_in_channels = 1
        if current_state.layers[start_layer_num].layer_type != LayerType.FULLY_CONNECTED:
            num_in_channels = int(layer_sizes[start_layer_num][-1])

        if current_state.layers[start_layer_num+1].layer_type == LayerType.CONVOLUTIONAL:
            link_values = SplitFilter(num_in_channels, weights[start_layer_num-weightless_layer]).tolist()
            return link_values
        elif current_state.layers[start_layer_num+1].layer_type == LayerType.POOLING:
            pool_size = reader.GetPoolSize(start_layer_num)
            link_values = np.full((pool_size[0], pool_size[1], num_in_channels, layer_sizes[start_layer_num+1][-1]), edge_representation.value).tolist()
            return link_values
    elif isinstance(edge_representation, SingleValueEdgeRepresentation):
        link_values = [edge_representation.value]
        return link_values

    #Defaults to Adjacency matrix representation
    if current_state.layers[start_layer_num+1].layer_type == LayerType.POOLING:
        for node in range(0, np.prod(layer_sizes[start_layer_num])):
            values = np.zeros(np.prod(layer_sizes[start_layer_num+1]))
            window_size = 2
            side_length = layer_sizes[start_layer_num][0]
            values[int(np.floor(node/window_size)%(0.5*side_length) + np.floor(node/(side_length*2))*0.5*side_length)] = 1
            link_values.append(values.tolist())

    if current_state.layers[start_layer_num+1].layer_type == LayerType.CONVOLUTIONAL:
        for node in range(0, np.prod(layer_sizes[start_layer_num])):
            values = np.zeros(np.prod(layer_sizes[start_layer_num+1])).tolist()
            link_values.append(values)

    if current_state.layers[start_layer_num+1].layer_type == LayerType.FULLY_CONNECTED:
        for node in range(0, np.prod(layer_sizes[start_layer_num])):
            values = weights[start_layer_num-weightless_layer][node].tolist()
            link_values.append(values)
    return link_values


def UseActivationAsLinkValues(activations, weights, layer_sizes, start_layer_num):
    """Assigns the links of a layer the corresponding activation outputs als values."""
    link_values = []

    for node in range(0, layer_sizes[start_layer_num]):
        values = (activations[start_layer_num][0][node] * weights[start_layer_num][node]).tolist()
        link_values.append(values)

    return link_values


def SetLinkValues(reader, layer_sizes, edge_representation, edge_visualization, connection_end, activations, state):
    """Gets the values of the links between two layers depending on the edge_visualisation enum."""
    if edge_visualization == EdgeVisualization.WEIGHTS:
        link_values = UseWeightsAsLinkValues(reader, layer_sizes, connection_end - 1, reader.GetWeights(), state, edge_representation)
    elif edge_visualization == EdgeVisualization.ACTIVATION and activations is not None:
        link_values = UseActivationAsLinkValues(activations, reader.GetWeights(), layer_sizes, connection_end - 1)
    else:
        link_values = UseWeightsAsLinkValues(reader, layer_sizes, connection_end - 1, reader.GetWeights(), state, edge_representation)
    return link_values
