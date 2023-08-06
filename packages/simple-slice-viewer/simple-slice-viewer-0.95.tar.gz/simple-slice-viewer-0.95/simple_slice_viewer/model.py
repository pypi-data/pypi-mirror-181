from PyQt5.QtCore import QAbstractListModel, pyqtSignal, QObject, Qt
import math
from simple_slice_viewer.logger import Logger
import numpy as np
import SimpleITK as sitk
import os
import sitk_tools



SUV = 'SUV'
CT = 'CT'
FULL = 'Full'
MASK = 'Mask'

AXIAL = 'Axial'
CORONAL = 'Coronal'
SAGGITAL = 'Saggital'

ORIENTATIONS = (SAGGITAL, CORONAL, AXIAL)

LOG_LEVEL = Logger.LEVEL_INFO


def load_image(image):
    if isinstance(image, str) and os.path.exists(image):
        image = sitk.ReadImage(image)
    elif isinstance(image, np.ndarray):
        image = sitk.GetImageFromArray(image)
    elif isinstance(image, sitk.Image) or image is None:
        pass
    else:
        raise TypeError(f'Cannot load image of type {type(image)}')
    return image


   
class ImageSlicer(QObject):
    _counter = 0
    _slice_index = None
    _frame_index = None
    
  
    _cached_image = None
    _cached_slice = None


    
    _image = None
    _array = None
    _view_direction = None
    
    slice_changed = pyqtSignal(int)
    
    
    frame_index_changed = pyqtSignal(int)
    image_changed = pyqtSignal()
    view_direction_changed = pyqtSignal(str)
    
    def __init__(self, image=None, 
                 view_direction=AXIAL, 
                 index=None, 
                 frame_index=None):
        
        QObject.__init__(self)
        
        
        self.set_image(image)
        self._set_view_direction(view_direction)
        self.set_slice_index(index)
        
    def get_clim(self):
        if self._image is None:
            return [0, 1]
        else:
            return [sitk_tools.min(self.get_image()), 
                    sitk_tools.max(self.get_image())]
        
    def get_slice_center_index(self):
        imslice = self.get_sitk_slice()
        if imslice is None:
            return [0, 0, 0]
        
        center = [round(si/2) for si in imslice.GetSize()]
        return center
    
    def get_image_index(self, index):
        if self.get_image() is None:
            return None
        elif len(index) == self.get_ndim():
            return index
        elif len(index) == 3 and self.get_ndim() == 4:
            return [*index, self.get_frame_index()]
        elif len(index) == 2 and self.get_ndim() >= 3:
            
            direction = self.get_view_direction()
        
            if direction == SAGGITAL:
                index = [self.get_slice_index(), *index]
            elif direction == CORONAL:
                index = [index[0], self.get_slice_index(), index[1]]
            elif direction == AXIAL:               
                index = [index[0], index[1], self.get_slice_index()]
            if self.get_ndim() == 4:
                return [*index, self.get_frame_index()]
            else:
                return index
        else:
            raise RuntimeError()
    
    def get_value_at_index(self, index):
        if self.get_image() is None:
            return None
        
        index = [math.floor(ii) for ii in index]
        
        if any([ii<0 for ii in index]):
            raise IndexError()    
            
        if len(index) == 2:
            image = self.get_sitk_slice()
        elif len(index) == 3:
            image = self.get_image()
        else:
            raise IndexError()
        
        return image[index]
        
    def transform_index_to_physical_point(self, index):
        image = self.get_image()
        if image is None:
            return None
        
        ndim = image.GetDimension()
        
        
        if image is None:
            phys = None
        elif ndim == 2:
            phys = image.TransformContinuousIndexToPhysicalPoint(index)
        elif ndim == 3:
            phys = (0, 0, 0)
            if len(index) == 3:
                phys = image.TransformContinuousIndexToPhysicalPoint(index)
            elif len(index) == 2:
                direction = self.get_view_direction()
                if direction == SAGGITAL:
                    index = [self.get_slice_index(), *index]
                elif direction == CORONAL:
                    index = [index[0], self.get_slice_index(), index[1]]
                elif direction == AXIAL:
                    # account for y flip in viewing
                    indexy = self.get_image().GetSize()[2]-  index[1]
                    index = [index[0], indexy, self.get_slice_index()]
                else:
                    raise RuntimeError()
            else:
                raise IndexError(f'Wrong number of values passed {len(index)}')
           
            phys = image.TransformContinuousIndexToPhysicalPoint(index)
            
        return np.round(np.asarray(phys), decimals=1).tolist()

    def __len__(self):
        return self.get_slice_count()
    
    def get_ndim(self):
        if self._image is None:
            ndim = 0
        else:
            ndim = self._image.GetDimension()
        return ndim
    
    def get_frame_index(self):
        if self.get_ndim() == 4:
            valid_index =  self._frame_index is not None\
                    and self._frame_index > 0\
                    and self._frame_index < self._image.GetSize()[3]
              
            if not valid_index:
                self._frame_index = 0
        else:
            self._frame_index = 0
                
        return self._frame_index
    
   
            
    def set_frame_index(self, index):
        if self._frame_index != index:
            
            self._cached_image = None
            self._cached_slice = None
            self._frame_index = index        
            self.emit_changed_frame_index()
        
    def emit_changed_frame_index(self):
        if self.get_frame_index() is not None:
            self.frame_index_changed.emit(self.get_frame_index())
            
    def get_number_of_frames(self):
        if self.get_ndim() == 0:
            return 0
        elif self.get_ndim() == 4:
            
            return self._image.GetSize()[3]
        else:
            return 1
    
    
    def get_slice_index(self):
        
        valid_index =  self._slice_index is not None\
                and self._slice_index >= 0\
                and self._slice_index < len(self)
          
        if not valid_index:
            self._slice_index = int(len(self)/2)
        
        return self._slice_index
    
    
    def set_slice_index(self, index):        
        if index is None:
            index = int(len(self)/2)

        index = int(index)
        
        if index == self._slice_index:
            return
        #self.logger.debug('start slice scroll to index: %s', str(index))        
        self._cached_slice = None
        self._slice_index = index
        self.slice_changed.emit(index)

    def get_slice(self, index, view_direction):        
        image = self.get_image()
        
        if image is None: return None
        
        if index is None: return None
        
        if image.GetDimension() == 2:
            return image
        
        try:
            if view_direction == SAGGITAL:
                imslice = image[index, :, : ]
            elif view_direction == CORONAL:
                imslice = image[:, index, : ]
            elif view_direction == AXIAL:
                imslice = image[:, :, index]
                imslice = sitk.Flip(imslice, [False, True])

        except IndexError:
            msg = 'Index {0} out of bound for image size {1} and direction {2}'
            raise IndexError(msg.format(str(index), str(image.GetSize()),
                                                     str(view_direction)))
        return imslice

    def get_sitk_slice(self):
        if self._cached_slice is None:
            direction = self.get_view_direction()
            index = self.get_slice_index()            
            self._cached_slice = self.get_slice(index, direction)
        return self._cached_slice
    
    def get_image(self):
        if self._cached_image is None:
            if self._image is not None and self.get_ndim() == 4:
                image = self._image[:, :, :, self.get_frame_index()]
                self._cached_image = image
            else:
                self._cached_image = self._image
        return self._cached_image
    
   
    def set_image(self, image):
        
        if image is self._image:
            return
      
        self._image = load_image(image)
        
        self._slice_index = None
        self._frame_index = None 
        self._cached_slice = None
        self._cached_image = None
        
        self.image_changed.emit()
      

    def get_view_direction(self):
        if self._view_direction is None:
            self._view_direction = AXIAL
        # if self.get_image() is None:
        #     self._view_direction = None

        return self._view_direction
    
    def _set_view_direction(self, view_direction):
        self._cached_image = None
        self._cached_slice = None
        self._view_direction = view_direction
        self.set_slice_index(None)
        self.view_direction_changed.emit(view_direction)
        
    def get_slice_count(self):
        if self.get_image() is None or self.get_image().GetDimension() < 3:
            return 0
        
        imsize = self.get_image().GetSize()
        view_direction = self.get_view_direction()
        if view_direction == AXIAL:
            return imsize[2]
        elif view_direction == CORONAL:
            return imsize[1]
        elif view_direction == SAGGITAL:
            return imsize[0]
        else:
            raise ValueError
            


class SyncedImageSlicers(QAbstractListModel):
    slice_changed = pyqtSignal(int)
    image_changed = pyqtSignal(int)
    cursor_changed = pyqtSignal(tuple)
    
    frame_index_changed = pyqtSignal(int)
    view_direction_changed = pyqtSignal(str)
    
    ImageRole = Qt.UserRole + 1
    FusionRole = Qt.UserRole + 1
    _cursor_index = None

    def __init__(self, images=None, view_direction=AXIAL, index=None,
                 frame_index=None):
        QAbstractListModel.__init__(self)
        
        if isinstance(images, sitk.Image):
            images = [images]
        
        if images is None:
            images = [None] * 2
        
        self._image_slicers = [ImageSlicer() for i in range(len(images))]
        
        for i, image in enumerate(images):
            self.set_image(i, image)
            
        self.set_view_direction(view_direction)

    def get_number_of_slices(self):
        return len(self[0])
    
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self[index].get_view_direction()
        elif role == self.ImageRole:
            return self[0].get_image()
        elif role == self.FusionRole:
            return self[1].get_image()
        
    def get_number_of_frames(self):
        if self[0].get_ndim() == 4:
            return self[0].get_number_of_frames()
        elif self[1].get_ndim() == 4:
            return self[1].get_number_of_frames()
        elif self[0].get_image() is not None:
            return 1
        else:
            return 0
 
    def __getitem__(self, index):
        return self._image_slicers[index]
    
    
    def set_view_direction(self, view_direction):    
        if view_direction == self[0].get_view_direction():
            return
        
        for i in range(0, len(self)):
            self[i]._set_view_direction(view_direction)

        self.view_direction_changed.emit(self.get_view_direction())
        
    def get_view_direction(self):
        if self.get_image(0) is None:
            return None
        else:
            return self[0].get_view_direction()
    
    def set_frame_index(self, index):
     
        if self[0].get_ndim() == 4:     
            self[0].set_frame_index(index)
        if self[1].get_ndim() == 4:
            self[1].set_frame_index(index)
      
        self.emit_changed_frame_index(index)
        
    def get_frame_index(self):
        if self[0].get_ndim() == 4:
            return self[0].get_frame_index()
        elif self[1].get_ndim() == 4:
            return self[1].get_frame_index()
        elif self[0].get_ndim() == 0 and self[1].get_ndim() == 0:
            return 0
        return 1
        
    def emit_changed_frame_index(self, index):
        if self[0].get_frame_index() is not None\
            or self[1].get_frame_index() is not None:
            self.frame_index_changed.emit(self[0].get_frame_index())
    
    def set_slice_index(self, index):
       
        self[0].set_slice_index(index)
        self[1].set_slice_index(index)
        
        self.slice_changed.emit(self[0].get_slice_index())

    def get_slice_index(self):
        return self[0].get_slice_index()
    

    def get_image(self, index=None):
        return self[index].get_image()
    
    def set_image(self, index, image):
       
        if index == 0:
            image = image
            fusion = self[1].get_image()
        elif index == 1:
            fusion = image
            image = self[0].get_image()
      
        if index == 0:
            self[0].set_image(image)
            if not sitk_tools.same_space(image, fusion):
                self[1].set_image(None)
            
            self[0].set_image(image)        
      
        if index == 1:
            if not None in (image, fusion):
                same_dimension = image.GetDimension() == fusion.GetDimension()
                if image.GetDimension() == 3 and fusion.GetDimension()==4:
                    same_dimension = True
                if not same_dimension:
                    print('Image and Fusion must have same dimension!')
                    return
            
                if not sitk_tools.same_space(image, fusion):                
                    fusion = sitk_tools.resample_to_image(fusion, 
                                                          ref_image=image)
                            
            self[1].set_image(fusion)        
        
        
       
        self.image_changed.emit(index)
        
        self.set_slice_index(None)    
      

    def __len__(self):
        return len(self._image_slicers)
    
if __name__ == "__main__":
    image = sitk.ReadImage('imslice.nii')
    model = SyncedImageSlicers()