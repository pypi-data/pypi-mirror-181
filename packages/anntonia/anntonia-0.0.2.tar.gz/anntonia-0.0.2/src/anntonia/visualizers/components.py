import math
from enum import Enum


class EdgeVisualization(Enum):
    """An enum for the different ways values can be assigned to links between nodes."""
    WEIGHTS = 0
    ACTIVATION = 1


class MatrixEdgeRepresentation:
    '''Encodes the edge values as an adjacency matrix'''

    def __init__(self):
        self.type = "AD_MATRIX"


class FilterEdgeRepresentation:
    '''Encode the edge values as a filter kernel'''

    def __init__(self, value=1):
        self.type = "FILTER"
        self.value = value


class SingleValueEdgeRepresentation:
    '''Encode the edge values as a single value to use for all edges. Default 0 for invisible edges'''

    def __init__(self, value=0):
        self.type = "SINGLE"
        self.value = value


class GridRepresentation:
    """Arranges the nodes within a layer in a rectangular grid."""
    def __init__(self, x_dim=None, y_dim=None):
        self.x_dim = x_dim
        self.y_dim = y_dim

    def SetSidesForSquare(self, number_of_entries):
        """Provides a function to calculate the length of the sides for a given number of entries."""
        self.x_dim = math.ceil(math.sqrt(number_of_entries))
        self.y_dim = self.x_dim


class DimRedRepresentation:
    """"Arranges the nodes by how they are related to one another in a layer using a dimension reduction."""
    def __init__(self, distance_algorithm=0, reduction_algorithm=0):
        self.distance_algorithm = distance_algorithm
        self.reduction_algorithm = reduction_algorithm


class LinearRepresentation:
    """Arranges the nodes in a single horizontal line. Used for the output layer in mnist models"""


class ConvRepresentation:
    """Arranges the nodes as a number of sublayers like convolutional layers are commonly depicted"""


class NodeVisualization(Enum):
    """An enum to select which values of the nodes are to be visualized."""
    PREV_WITH_ACTIVATION = 0
    PREV_WITHOUT_ACTIVATION = 1
    BIAS = 2