from anntonia.visualizers.components import GridRepresentation, DimRedRepresentation, LinearRepresentation, ConvRepresentation
from anntonia.visualizers.data_transformation import *
from anntonia.utils.dimensionality_reduction import *


def GetNodeCoordinatesInGrid(layer_representation, layer_size):
    """Computes the coordinates of the nodes for a grid arrangement."""
    if layer_representation.x_dim is None or layer_representation.y_dim is None:
        layer_representation.SetSidesForSquare(layer_size)
    coordinates = []
    counter = 0
    for x_coord in range(layer_representation.x_dim):
        for y_coord in range(layer_representation.y_dim):
            if counter >= layer_size:
                break
            coordinates.append([x_coord/layer_representation.x_dim, y_coord/layer_representation.y_dim])
            counter += 1
    return coordinates


def GetNodeCoordinatesWithDimRed(model_reader, test_data, layer_num, layer_size,
                                 distance_algorithm=0, reduction_algorithm=0):
    """Computes the coordinates of the nodes for an arrangement based on on a dimension reduction"""
    activation_output = model_reader.GetActivationOutput(test_data[(test_data.shape[0] - 1000):], layer_num)
    dissimilarity_matrix = GetDissimilarityMatrix(activation_output, distance_algorithm)
    dim_reduction = GetDimensionReduction(dissimilarity_matrix, reduction_algorithm)
    dim_red_coords = CalculateNodeCoordinates(dim_reduction, 28, layer_num, layer_size)

    node_coordinates = []
    for node in range(0, layer_size):
        coordinates = dim_red_coords[node]
        node_coordinates.append((coordinates[1], coordinates[2]))

    return node_coordinates


def GetNodeCoordinatesLinear(layer_size):
    node_coordinates = []
    for node in range(layer_size):
        node_coordinates.append((0, node))
    return node_coordinates


def GetNodeCoordinatesConv(layer_shape):
    """Computes the node coordinates by creating a row of sublayers that is aligned along the diagonal of the layer. Expects the shape to be (dimensions1, dimensions2, number of sublayers)"""
    node_coordinates = []
    layer_size = np.prod(layer_shape)
    for node in range(layer_size):
        node_coordinates.append((int(node/layer_shape[0]), node%layer_shape[1] + int(node/np.prod(layer_shape[:2]))*layer_shape[1]))
    return node_coordinates


def SetNodeCoordinates(layer_representation, layer_num, layer_size, reader, test_data):
    """Gets the coordinates for the nodes in a layer, depending on the layer_representation object."""
    if isinstance(layer_representation, GridRepresentation):
        node_coordinates = GetNodeCoordinatesInGrid(layer_representation, np.prod(layer_size))
    elif isinstance(layer_representation, DimRedRepresentation):
        node_coordinates = GetNodeCoordinatesWithDimRed(reader, test_data, layer_num, np.prod(layer_size),
                                                        layer_representation.distance_algorithm,
                                                        layer_representation.reduction_algorithm)
    elif isinstance(layer_representation, LinearRepresentation):
        node_coordinates = GetNodeCoordinatesLinear(np.prod(layer_size))
    elif isinstance(layer_representation, ConvRepresentation):
        node_coordinates = GetNodeCoordinatesConv(layer_size)
    else:
        print(f"Representation for layer {layer_num} not recognized.")
        node_coordinates = GetNodeCoordinatesInGrid(GridRepresentation(), np.prod(layer_size))
    return node_coordinates
