from anntonia.visualizers.linear_model.node_coordinates import *
from anntonia.visualizers.linear_model.node_values import *
from anntonia.visualizers.linear_model.edges import *
from anntonia.visualizers.data_transformation import *
from anntonia.server.state import State, Layer, Connection


class LinearModelVisualizer():
    """Starts a server that visualizes a given linear model.

    Keyword arguments:
    reader -- a reader object that can access the model, such as a KerasReader from ANNtoNIA_Keras
    test_data -- input data
    layer_representations -- how the nodes in each layer should be arranged (default: all default_grid)
    edge_representations -- how the edges and edge values should be encoded (default: MatrixEdgeRepresentation)
    edge_visualization -- which values are to be visualized on the edges (default: EdgeVisualization.WEIGHTS)
    node_visualization -- which values should be visualized on the nodes of each layer (default: all values to 0)
    actions -- the actions the server can respond to (default: test_actions)
    propagation_image -- the image the activations are calculated for (default: None)
    propagation_image_label --  the label found for propagation_image, when this is set
                                layer-wise relevance propagation is used (default: None)"""

    def __init__(self, reader, test_data, layer_representations=None, edge_representations=None,
                 edge_visualization=EdgeVisualization.WEIGHTS,
                 node_visualization=None, propagation_image=None, propagation_image_label=None):
        self.model = reader
        self.alternative_model = self.model
        self.epoch_of_alternative = None
        self.state = State()

        self.layer_sizes = self.model.GetLayerSizes()  # tupel of all layer shapes
        self.weighted_layer_sizes = self.model.GetWeightedLayerSizes()  # tupel of all layer shapes that have weights
        self.number_of_layers = len(self.layer_sizes)
        self.activations = None
        self.edge_representations = edge_representations
        self.edge_visualization = edge_visualization

        if layer_representations is None:
            layer_representations = [GridRepresentation() for layer in range(self.number_of_layers + 1)]

        if node_visualization is None:
            node_visualization = [NodeVisualization.BIAS for layer in range(self.number_of_layers + 1)]

        if edge_visualization == EdgeVisualization.ACTIVATION and propagation_image is not None:
            self.activations = ComputeActivationOutput(self.model, propagation_image, propagation_image_label)

        # always create a layer for the input. Needed because the first layer is not always a weightless layer that substitutes the input
        propagation_image = np.asarray(propagation_image)
        input_layer = Layer()
        input_layer.node_coordinates = SetNodeCoordinates(layer_representations[0], 0, propagation_image.shape,
                                                          self.model, test_data)
        input_layer.node_values = InputAsNodeValues(propagation_image)
        self.state.layers.append(input_layer)

        weighted_layer_num = 0  # keeps track of the index of the current weighted layer
        droppedLayers = 0  # keeps track of the number of supporting layers that were dropped

        for layer_num, layer_size in enumerate(self.layer_sizes):
            layer = Layer()
            self.SetLayerType(layer_num, layer)
            # check if the layer only plays a supporting role (e.g. Flatten layers) and should not be taken into account
            if layer.layer_type != LayerType.SUPPORTING:
                try:
                    layer.node_coordinates = SetNodeCoordinates(layer_representations[layer_num + 1 - droppedLayers],
                                                                layer_num, layer_size, self.model, test_data)
                except IndexError:
                    raise IndexError(
                        'The number of layers and entries of layer_representations do not match. Note that the input layer also needs a Representation, even if it is not specified in the model')

                layer.node_values = SetNodeValues(node_visualization[layer_num + 1 - droppedLayers], self.model,
                                                  self.weighted_layer_sizes, weighted_layer_num, layer_num,
                                                  self.state.layers[layer_num - droppedLayers], layer.layer_type)
                if layer.layer_type != LayerType.POOLING:
                    weighted_layer_num += 1
                self.state.layers.append(layer)
            else:
                droppedLayers += 1

        self.RemoveSupportingLayers()
        self.number_of_layers += 1  # Account for extra input layer
        self.layer_sizes.insert(0, propagation_image.shape)  # Adds shape of input to layer_sizes list

        if edge_representations is None:
            self.edge_representations = [MatrixEdgeRepresentation() for connection in range(self.number_of_layers - 1)]

        for connection_end in range(1, self.number_of_layers):
            connection = Connection()

            try:
                if isinstance(self.edge_representations[connection_end - 1], FilterEdgeRepresentation):
                    if self.state.layers[connection_end].layer_type == LayerType.FULLY_CONNECTED:
                        print("FilterEdgeRepresentation is not supported with fully connected layers")
                        self.edge_representations[connection_end - 1] = MatrixEdgeRepresentation()
                    else:
                        connection.stride = [i for i in self.model.GetStride(connection_end - 1)]
                connection.connection_type = self.edge_representations[connection_end - 1].type
            except IndexError:
                raise IndexError("The number of connections and entries of edge_representations do not match")
            except AttributeError:
                print(f"Unknown edge representation for connection from layer {connection_end - 1} to {connection_end}")
                self.edge_representations[connection_end - 1] = MatrixEdgeRepresentation()
                connection.connection_type = self.edge_representations[connection_end - 1].type

            connection.visualize_on_start = (self.state.layers[
                                                 connection_end].layer_type != LayerType.CONVOLUTIONAL)  # On default, don't visualize convolutional layer
            connection.sum_channels = (self.state.layers[
                                           connection_end].layer_type != LayerType.POOLING)  # On default, only pool channel wise
            connection.link_values = SetLinkValues(self.model, self.layer_sizes,
                                                   self.edge_representations[connection_end - 1],
                                                   self.edge_visualization,
                                                   connection_end, self.activations, self.state)

            self.state.connections[(connection_end - 1, connection_end)] = connection
        # print(f"Recognized Digit: {np.argmax(self.state.layers[-1].node_values)} || Actual Digit: {propagation_image_label}")

    def GetModel(self):
        return self.model

    def GetEpochOfAlternative(self):
        if self.epoch_of_alternative is None:
            for number, model in enumerate(self.model.GetEpochs()):
                if model.path == self.alternative_model.path:
                    self.epoch_of_alternative = number
        return self.epoch_of_alternative

    def SetAlternativeModel(self, model):
        self.alternative_model = model

    def UseAlternativeConnectionValues(self):
        for (start, end) in self.state.connections:
            new_values = SetLinkValues(self.alternative_model, self.layer_sizes, self.edge_representations[start],
                                       self.edge_visualization, end, self.activations, self.state)
            if new_values is not self.state.connections[(start, end)].link_values:
                self.state.connections[(start, end)].link_values = new_values
        print("Connection values adjusted.")

    def SetLayerType(self, layer_num, layer):
        layer.layer_type = self.model.GetLayerType(layer_num)

    def RemoveSupportingLayers(self):
        '''Removes all layers of LayerType "SUPPORTING", adjusts number_of_layers and removes the shapes from the layer_sizes list'''
        for num in range(self.number_of_layers):
            layer = Layer()
            self.SetLayerType(num, layer)
            if layer.layer_type == LayerType.SUPPORTING:
                self.number_of_layers -= 1
                del self.layer_sizes[num]
