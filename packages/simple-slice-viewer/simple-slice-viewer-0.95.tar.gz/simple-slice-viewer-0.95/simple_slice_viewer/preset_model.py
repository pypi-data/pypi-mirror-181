import os
import yaml
import numpy as np
import inspect
from copy import copy
import pyqtgraph as pg
import matplotlib.pyplot as plt
from PyQt5.QtCore import QAbstractListModel, pyqtSignal, QObject

try:
    CONFIG_FOLDER = os.path.split(__file__)[0]
    print(CONFIG_FOLDER, 'a')
except:
    CONFIG_FOLDER = os.getcwd()
    print(CONFIG_FOLDER, 'b')


from PyQt5.QtCore import Qt

CONFIG_FILE = os.path.join(CONFIG_FOLDER, 'presets.yml')
CONFIG = yaml.safe_load(open(CONFIG_FILE))


class QModelItem(QObject):
    _defaults = {}
    value_changed = pyqtSignal(list)

    def __init__(self, **kwargs):
        super().__init__()
        
        self.set_defaults()
        self.update(**kwargs)
    
    def __copy__(self):
        copy_dict = {}
        for key in self._defaults.keys():
            value = getattr(self, key)
            if isinstance(value, QModelItem):
                value = copy(value)
                
            copy_dict[key] = value
        return self.__class__(**copy_dict)
    
    def copy(self):
        return copy(self)
    
    def __str__(self):
        return(yaml.dump(dict(self)))
        
    def __iter__(self):
        for key in self._defaults.keys():
            value = getattr(self, key)
            if isinstance(value, QModelItem):
                value = dict(value)
            yield (key, value)
            
    def set_defaults(self):
        for key, value in self._defaults.items():
            if inspect.isfunction(value) or inspect.isclass(value):
                value = value()
            setattr(self, key, value)
            
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
    
 
    
    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)
    
class ColorScale(QModelItem):
    #Keys
    PARENT_KEY      = 'colorscale'
    SCALE           = 'scale'
    NAME            = 'name'
    SCALE_TYPE      = 'scale_type'
    
    # Scale Types
    WINDOW_LEVEL             = 'window_level'
    RELATIVE_MIN_MAX         = 'relative_max'
    FIXED                    = 'fixed'
        
    DEFAULT_NAME    = 'colorscale'

    _defaults = {SCALE_TYPE:    RELATIVE_MIN_MAX,
                 NAME:          DEFAULT_NAME,
                 SCALE:         ['0%', '100%']}
                 
    def get_clim(self, clim_range=None):
        if self.scale_type == self.WINDOW_LEVEL:
            clim = [self.scale[1] - 0.5 * self.scale[0],
                    self.scale[1] + 0.5 * self.scale[0]]            
        elif self.scale_type == self.RELATIVE_MIN_MAX:
            scale = [float(ii.replace('%', '')) if isinstance(ii, str) else ii\
                     for ii in self.scale]
                     
            clim = [scale[0]/100 * clim_range[0],
                    scale[1]/100 * clim_range[1]]
        elif self.scale_type == self.FIXED:
            clim = [*self.scale]
    
        return clim    

        
class ImagePreset(QModelItem):
    GREENS = 'greens'
    MAGENTAS = 'magentas'
    WINDOW_LEVEL_NAME = 'window_level_name'
    COLORMAP = 'colormap'
    COLORSCALE = 'colorscale'
    ALPHA = 'alpha'
    NAME = 'name'
    
    _defaults = {NAME: 'ImagePreset', 
                 COLORSCALE: ColorScale, 
                 COLORMAP: 'gray', 
                 ALPHA: 1}
    
    _greens = np.array([[0., 0., 0., 0.],
                          [0., 1., 0., 1.]])

    _magentas = np.array([[0., 0., 0., 0.],
                          [1., 0., 1., 1.]])
    
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
    
    @classmethod
    def get_available_colormaps(cls):
        cmaps = plt.colormaps()
        cmaps += ['greens', 'magentas']        
        cmaps = sorted(list(set(cmaps)))
        return cmaps
    
    @staticmethod
    def _get_cmap(col_data):
        return pg.ColorMap(pos=col_data[:,-1], color=255*col_data[:,:3]+0.5)
    
    @property
    def pg_colormap(self):
        return self.get_pg_colormap(self.colormap)
    
    @classmethod
    def from_dict(cls, dct):
        dct[ColorScale.PARENT_KEY] = ColorScale.from_dict(dct[ColorScale.PARENT_KEY])
        return super().from_dict(dct)
    
    
    @classmethod
    def get_pg_colormap(cls, cmap):
        if isinstance(cmap, pg.ColorMap):
            return cmap
        if cmap == cls.GREENS:
            return cls._get_cmap(cls._greens)
        elif cmap == cls.MAGENTAS:
            return cls._get_cmap(cls._magentas)
        elif cmap is None:
            cmap = 'gray'
            
        
        return pg.colormap.getFromMatplotlib(cmap)

class ImageFusionPreset(QModelItem):
    IMAGE_PRESET = 'image_preset'
    FUSION_PRESET = 'fusion_preset'
    NAME = 'name'
    
    _defaults = {IMAGE_PRESET: 'image_preset',
                 FUSION_PRESET: 'fusion_preset',
                 NAME: 'ImageFusionPreset'}
    
    def __init__(self, **kwargs):
        if self.IMAGE_PRESET not in kwargs.keys() or kwargs[self.IMAGE_PRESET] is None:
            kwargs[self.IMAGE_PRESET] = 'Min-Max'
        
        if self.FUSION_PRESET not in kwargs.keys() or kwargs[self.FUSION_PRESET] is None:
            kwargs[self.FUSION_PRESET] = 'Min-Max'
            
        super().__init__(**kwargs)
            

class QModelItemList(QAbstractListModel):
    PARENT_KEY = 'item_list'
    
    ITEM_CLASS = QModelItem
    DEFAULT_ITEM_NAME = 'name'
    DISPLAY_ROLE_KEY = 'name'
    
    NAME = 'name'
    
    
    presetChanged = pyqtSignal(str)
    nameChanged = pyqtSignal(str, str)
    
    _index = 0
    
    def __init__(self, *args, item_list=None, **kwargs):
        QAbstractListModel.__init__(self, *args, **kwargs)
        self.item_list = item_list or []
        
    def __str__(self):
        return(yaml.dump(self.to_list()))
        
    def __iter__(self):
        return self.item_list.__iter__()
    
    def __getitem__(self, indices):
        return self.item_list.__getitem__(indices)
    
    def __len__(self):
        return len(self.item_list)
    
    def __copy__(self):
        return self.__class__.from_list([copy(item) for item in self.item_list])
    
    def update(self, model_list, *args, **kwargs):
        for item in model_list:
            self.item_list.append(self.ITEM_CLASS.from_dict(dict(item), *args, **kwargs))
        self.layoutChanged.emit()
    
    def get_names(self):
        return [item.name for item in self]
    
    def get_index(self):
        return self.index(0).column()
    
    def copy(self):
        return copy(self)
        
    def clear(self):
        self.beginResetModel()
        while len(self) > 0:
            self.delete(0)
        self.endResetModel()
    
    def get_new_name(self):
        name = self.DEFAULT_ITEM_NAME        
        i = 0
        while name in [item.name for item in self]:
            i += 1
            name = self.DEFAULT_ITEM_NAME + str(i)
        return name
    
    def new_item(self):
        item = self.ITEM_CLASS(name=self.get_new_name())
        return item
    
    def data(self, index, role): 
        if index.isValid() and role==Qt.DisplayRole:            
            value =  getattr(self.item_list[index.row()], self.DISPLAY_ROLE_KEY)
            return value
        
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            if role == Qt.EditRole and value is not None:    
                value = dict(value)
                if self.NAME in value.keys():
                    old_name = self.data(index, role=Qt.DisplayRole)
                self.item_list[index.row()].update(**value)
                self.dataChanged.emit(index, index, [Qt.EditRole])
                if self.NAME in value.keys():
                    self.nameChanged.emit(old_name, value[self.NAME])
                    
    def rowCount(self, index):
        return len(self.item_list)
    
    def add(self, index=None):
       
        item = self.new_item()
       
        if index is None:
            self.item_list.append(item)
        else:
            self.item_list.insert(index, item)
       
        self.layoutChanged.emit()
    
    def delete(self, index):
        if isinstance(index, QModelItem):
            index = [i for i, item in enumerate(self.item_list)\
                     if item.name == index.name][0]
        

        del self.item_list[index]    

                
        self.layoutChanged.emit()
        

    def roleNames(self):
        return self.Roles
    
    @classmethod
    def from_list(cls, item_list):  
        obj_list = []
        for item in item_list:
            if isinstance(item, dict):
                item = cls.ITEM_CLASS.from_dict(item)
            elif isinstance(item, cls.ITEM_CLASS):
                pass
            else:
                raise TypeError(f'Cannot Load Type {type(item)}')
            obj_list.append(item)
                    
        return cls(item_list=obj_list)
    
    
    def to_list(self):
        return [dict(item) for item in self.item_list]
    
    def get_item_by_value(self, attr, value):
        items = [item for item in self.item_list\
                 if getattr(item, attr) == value]
        
        if len(items) == 0:
            return None
            #raise IndexError(f'No Item has value {value} for attr {attr}')
        
        return items[0]
    
    def get_item_by_name(self, name):
        return self.get_item_by_value('name', name)
    
    @classmethod
    def from_defaults(cls):
        return cls.from_list(CONFIG[cls.PARENT_KEY])
    

class ColorScales(QModelItemList):    
    ITEM_CLASS = ColorScale
    PARENT_KEY = 'colorscales'
    DEFAULT_ITEM_NAME = 'color scale'
    NAME = 'name'
    
    

    
# class WindowLevels(NamedModelItemSequence):
#     ITEM_CLASS = ColorScale

class ImagePresets(QModelItemList):
    PARENT_KEY = 'image_presets'
    ITEM_CLASS = ImagePreset
    
    def get_colorscale_by_name(name, colorscales):
        scales = [scale for scale in colorscales if scale.name==name]
        if len(scales) == 0:
            scale = None
        else:
            scale = scales[0]
        return scale



class FusionPresets(ImagePresets):
    PARENT_KEY = 'fusion_presets'
    ITEM_CLASS = ImagePreset

class ImageFusionPresets(QModelItemList):
    IMAGE_PRESET = 'image_preset'
    FUSION_PRESET = 'fusion_preset'
    PARENT_KEY = 'image_fusion_presets'
    ITEM_CLASS = ImageFusionPreset

    def get_image_presets(self, image_presets):
        presets = []
        for item in self:
            preset = [preset for preset in image_presets\
                      if preset.name == item.image_preset][0]
            presets.append(preset)
        return presets
    
    def get_fusion_presets(self, fusion_presets):
        presets = []
        for item in self:
            preset = [preset for preset in fusion_presets\
                      if preset.name == item.fusion_preset][0]
            presets.append(preset)
        return presets

    def get_image_preset(self, index, image_presets):        
        return self.get_image_presets(image_presets)[index]
    
    def get_fusion_preset(self, index, fusion_presets):        
        return self.get_fusion_presets(fusion_presets)[index]
            


    

class PresetModel:
    FOLDER = '.simple-slice-viewer'
    FILE = 'presets.yml'
    def __init__(self, image_presets=None,
                  fusion_presets=None, image_fusion_presets=None,
                  colormaps=None):
        
        if colormaps is None:
            colormaps = []
            
       
        if image_presets is None:
            image_presets = ImagePresets()
            
        if fusion_presets is None:
            fusion_presets = ImagePresets()
            
        if image_fusion_presets is None:
            image_fusion_presets = ImageFusionPresets()
        
        self.colormaps = colormaps
        
        self.image_presets = image_presets
        self.fusion_presets = fusion_presets
        self.image_fusion_presets = image_fusion_presets
        self.set_callbacks()
    
    def set_callbacks(self):        
        self.image_presets.nameChanged.connect(self.image_preset_name_changed)
        self.fusion_presets.nameChanged.connect(self.fusion_preset_name_changed)
    
    def image_preset_name_changed(self, old_name, new_name):
        for item in self.image_fusion_presets:
            if item.image_preset == old_name:
                item.image_preset = new_name
                
    def fusion_preset_name_changed(self, old_name, new_name):
        for item in self.image_fusion_presets:
            if item.fusion_preset == old_name:
                item.fusion_preset = new_name
                    
   
    def get_used_imagepreset_names(self):
        used = []
        for item in self.image_fusion_presets:
            used += [item.image_preset]
        return sorted(list(set(used)))
    
    def get_used_fusionpreset_names(self):
        used = []
        for item in self.image_fusion_presets:
            used += [item.fusion_preset]
        return sorted(list(set(used)))
    
    def clear(self):
        self.image_fusion_presets.clear()
        self.fusion_presets.clear()
        self.image_presets.clear()
        self.colormaps.clear()
        
    def to_dict(self):
        dct = {}

        dct[ImagePresets.PARENT_KEY] = self.image_presets.to_list()
        dct[FusionPresets.PARENT_KEY] = self.fusion_presets.to_list()
        dct['colormaps'] = self.colormaps
        key = ImageFusionPresets.PARENT_KEY                           
        dct[key] = self.image_fusion_presets.to_list()
       
        
       
        return dct

    @classmethod
    def from_dict(cls, dct):
        colormaps               = dct['colormaps']
        image_presets           = dct[ImagePresets.PARENT_KEY]
        fusion_presets          = dct[FusionPresets.PARENT_KEY]
        image_fusion_presets    = dct[ImageFusionPresets.PARENT_KEY]
        
        
        
        image_presets = ImagePresets.from_list(image_presets)                                             
        fusion_presets = ImagePresets.from_list(fusion_presets)
        presets = ImageFusionPresets.from_list(image_fusion_presets)
                                               
        return cls(image_presets=image_presets,
                   fusion_presets=fusion_presets, 
                   image_fusion_presets=presets,
                   colormaps=colormaps)
    
    @classmethod
    def get_folder(cls):
        user_folder = os.path.expanduser('~')
        folder = os.path.join(user_folder, cls.FOLDER)
        return folder
    
    @classmethod
    def get_filename(cls):
        return os.path.join(cls.get_folder(), cls.FILE)
        
    def save_to_disk(self):
        os.makedirs(self.get_folder(), exist_ok=True)
        yaml.dump(self.to_dict(), open(self.get_filename(), 'w'))
    
    def restore_defaults(self):
        self.clear()
        file = CONFIG_FILE
        dct = yaml.safe_load(open(file))
        self.update(dict(self.from_dict(dct)))
        return self
    

    @classmethod
    def load_from_disk(cls, load_defaults=False):        
        file = cls.get_filename()
        if not load_defaults:
            try:
                dct = yaml.safe_load(open(file))
                print('Presets Loaded From Disk!')
            except:
                print('Loading Defaults')
                dct = yaml.safe_load(open(CONFIG_FILE))
        else:
            dct = yaml.safe_load(open(CONFIG_FILE))
            
        return cls.from_dict(dct)
    
    
    
if __name__ == "__main__":
    presets = PresetModel.load_from_disk(load_defaults=True)
    

