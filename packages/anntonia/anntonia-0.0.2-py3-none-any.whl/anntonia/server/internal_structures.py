class LayerList(list):
    '''Special list to manage layers and which of their attributes need their visualization to be updated.'''
    def __init__(self, *args, **kwargs):
        self._value_dirty = False
        self._coords_dirty = False
        self._mesh_dirty = False
        super(LayerList, self).__init__(*args, **kwargs)

    def append(self, __object):
        self._value_dirty = True
        self._coords_dirty = True
        self._mesh_dirty = True
        super(LayerList, self).append(__object)

    def remove(self, __value):
        self._value_dirty = True
        self._coords_dirty = True
        self._mesh_dirty = True
        super(LayerList, self).remove(__value)

    @property
    def value_dirty(self):
        for item in self:
            if hasattr(item, 'value_dirty'):
                if item.value_dirty is True:
                    self._value_dirty = True
        return self._value_dirty

    @property
    def coords_dirty(self):
        for item in self:
            if hasattr(item, 'coords_dirty'):
                if item.coords_dirty is True:
                    self._coords_dirty = True
        return self._coords_dirty

    @property
    def mesh_dirty(self):
        for item in self:
            if hasattr(item, 'mesh_dirty'):
                if item.mesh_dirty is True:
                    self._mesh_dirty = True
        return self._mesh_dirty

    @value_dirty.setter
    def value_dirty(self, bool):
        self._value_dirty = bool

    @coords_dirty.setter
    def coords_dirty(self, bool):
        self._coords_dirty = bool

    @mesh_dirty.setter
    def mesh_dirty(self, bool):
        self._mesh_dirty = bool


class ConnectionDict(dict):
    '''Special Dictionary to manage connections and if their visualization needs to be updated.'''
    def __init__(self, *args, **kwargs):
        self._dirty = False
        super(ConnectionDict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        self._dirty = True
        super(ConnectionDict, self).__setitem__(key, value)

    @property
    def dirty(self):
        for item in self.values():
            if hasattr(item, 'dirty'):
                if item.dirty is True:
                    self._dirty = True
        return self._dirty

    @dirty.setter
    def dirty(self, bool):
        self._dirty = bool