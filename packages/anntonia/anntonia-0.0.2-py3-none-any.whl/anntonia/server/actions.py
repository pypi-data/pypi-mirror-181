class SimpleAction():
    '''Class to represent a simple action that is called without parameters.'''
    
    def __init__(self, name, function):
        self.name = name
        self.function = function
        
    def Call(self, request):
        self.function()
        
class FloatAction():
    '''Class to represent a float action that is called with one float as the parameter.'''
    
    def __init__(self, name, function):
        self.name = name
        self.function = function
        
    def Call(self, request):
        param = float(request["parameter"])
        self.function(param)
        
class NodeAction():
    '''Class to represent a node action that is called with a single node as parameter.'''
    
    def __init__(self, name, function):
        self.name = name
        self.function = function
        
    def Call(self, request):
        layer_index = int(request["layer_index"])
        node_index = int(request["node_index"])
        self.function(layer_index, node_index)

class TextureAction():
    '''Class to represent a texture action that is called with an 3D array of color values'''
    
    def __init__(self, name, function):
        self.name = name
        self.function = function
        
    def Call(self, request):
        colors = request["colors"]
        self.function(colors)
        
