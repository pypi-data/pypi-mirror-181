from enum import Enum
from anntonia.server.internal_structures import LayerList, ConnectionDict


class LayerType(Enum):
    '''An Enum for the different types of layers'''
    FULLY_CONNECTED = 0 #Layers that are fully connected e.g. Dense in Keras
    CONVOLUTIONAL = 1 #Layers that create convolutions e.g. Conv2D in Keras
    POOLING = 2 #Pooling Layers e.g. MaxPooling2D in Keras
    SUPPORTING = 3  #Layers that are not to be viauslized but are needed for other purposes e.g. Reshape or Flatten in Keras


class Layer():
    '''Class to encapsulate all information that is relevant to one layer of the network.'''

    def __init__(self):
        self.node_values = []      # one float value for each node to be used for coloring nodes (activation, feature relevance, ...) or empty list if the feature is not used
        self.node_coordinates = []  # the coordinates of the nodes in 2D space as a list of float tuples
        self.node_mesh = "SPHERE"  # which static mesh to use for the neurons. SPHERE for the sphere mesh, CUBE for the cube mesh, Default is SPHERE
        self.layer_type = LayerType.FULLY_CONNECTED
        self.dirty = False
        self.value_dirty = False
        self.coords_dirty = False
        self.mesh_dirty = False
        

    def __setattr__(self, key, value):
        if key == "node_values" or key == "node_coordinates" or key == "node_mesh":
            self.dirty = True
            if key == "node_values":
                self.value_dirty = True
            elif key == "node_coordinates":
                self.coords_dirty = True
            elif key == "node_mesh":
                self.mesh_dirty = True
        super(Layer, self).__setattr__(key, value)


class Connection():
    '''Class to encapsulate all information that is relevant to the connection between two layers in the network.'''

    def __init__(self):
        self.link_values = []     # list of lists of floats to represent the value of each link to be used for visualizing the edges (neural network weights, relevance propagation, ...)
        self.connection_type = "AD_MATRIX" #How the link_values are supposed to be interpreted, default is adjacency matrix. All supported types are listed in functions.visualization
        self.stride = 0 #The stride used if this connection belongs to a pooling or convolutional layer (i.e. the destination layer is either a pooling or a convolutional layer)
        self.sum_channels = True #How to handle different input channels i.e. sum across them or only consider one (e.g. in pooling)
        self.visualize_on_start = True
        self.dirty = False

    def __setattr__(self, key, value):
        if key != "dirty":
            self.dirty = True
        super(Connection, self).__setattr__(key, value)


class State():
    '''Class to encapsulate all information that should be synchronized with the visualizer application.'''
    
    def __init__(self):
        self._layers = LayerList()            # list of all the network's layers
        self._connections = ConnectionDict()       # dictionary of all the network's connections, indexed by a tuple of indices (of self.layers) identifying the layers to be connected.
        self._dirty = True
        self._pad_dirty = False
        self._needs_drawing_pad = False         # bool to tell if the model needs the drawing pad

    def flush(self):
        for layer in self._layers:
            layer.coords_dirty = False
            layer.value_dirty = False
            layer.mesh_dirty = False
        for connection in self.connections.values():
            connection.dirty = False
        self._connections.dirty = False
        self._layers.value_dirty = False
        self._layers.coords_dirty = False
        self._layers.mesh_dirty = False
        self._pad_dirty = False
        self._dirty = False

    def GetLayerCount(self):
        return len(self._layers)
        
    def GetLayerSize(self, layer_index):
        return len(self.layers[layer_index].node_coordinates)

    def UpdateConnections(self):
        '''Call to visualize updated connection data'''
        self.connections.dirty = True

    def UpdateNodeValues(self):
        '''Call to visualize updated node values'''
        self.layers.value_dirty = True

    def UpdateNodeCoordinates(self):
        '''Call to visualize updated node coordinates'''
        self.layers.coords_dirty = True
    
    def UpdateNodeMeshes(self):
        '''Call to visualize updated node meshes'''
        self.layers.mesh_dirty = True

    @property
    def dirty(self):
        if self._connections.dirty is True or self._layers.value_dirty is True or self._layers.coords_dirty or self._layers.mesh_dirty is True:
            self._dirty = True
        return self._dirty

    @property
    def pad_dirty(self):
        return self._pad_dirty

    @property
    def layers(self):
        return self._layers

    @property
    def connections(self):
        return self._connections

    @property
    def needs_drawing_pad(self):
        return self._needs_drawing_pad

    @layers.setter
    def layers(self, new_layers):
        self._layers.value_dirty = True
        self._layers.coords_dirty = True
        self._layers.mesh_dirty = True
        if not isinstance(new_layers, LayerList):
            self._layers = LayerList(new_layers)
        else:
            self._layers = new_layers

    @connections.setter
    def connections(self, new_connections):
        self._connections.dirty = True
        if not isinstance(new_connections, ConnectionDict):
            self._connections = ConnectionDict(new_connections)
        else:
            self._connections = new_connections

    @needs_drawing_pad.setter
    def needs_drawing_pad(self, bool):
        if self._needs_drawing_pad != bool : self._pad_dirty = True
        self._needs_drawing_pad = bool

