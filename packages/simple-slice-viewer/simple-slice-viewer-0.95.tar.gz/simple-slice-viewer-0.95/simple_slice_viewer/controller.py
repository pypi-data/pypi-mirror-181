from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
import os
import SimpleITK as sitk
import sitk_tools
import pyqtgraph as pg
from simple_slice_viewer.movie_maker import MovieMaker
from simple_slice_viewer.view import SliceViewerWidget, MainView
from simple_slice_viewer.model import SyncedImageSlicers, AXIAL, CORONAL, SAGGITAL
from simple_slice_viewer.menus import MenuBar
from simple_slice_viewer.preset_controllers import StyleController
from simple_slice_viewer.preset_model import PresetModel
from simple_slice_viewer.preset_view import AvailableColorScaleDialog
from simple_slice_viewer.controller_base import ControllerBase
from simple_slice_viewer.load_pet_view import LoadPETController




SUPPORTED_FILES = ("Nifti Files (*.nii;*.nii.gz;*.nia;*.img;*.img.gz;*.hdr);;"
                   "Nrrd (*.nrrd;*.nhdr);;"
                   "Meta Image (*.mhd;*.mha);;"
                   "All Files (*)")


class FrameScrollController(ControllerBase):
    def __init__(self, *args, **kwargs):
        
        
        super().__init__(*args, **kwargs)
        
        self.update_scrollbar()
        
        self.view.framescroller.scrollbar.setValue(self.model.get_frame_index())
       
        index = self.model.get_frame_index()

        self.view.framescroller.scrollbar.setValue(index)
   
    
    def update_scrollbar(self):
        if self.model[0].get_ndim() == 4 or self.model[1].get_ndim() ==4:

            self.view.framescroller.setVisible(True)            
            self.view.framescroller.scrollbar.setMaximum(self.model.get_number_of_frames()-1)
            self.view.framescroller.value = self.model.get_frame_index()
           
        else:

            self.view.framescroller.setVisible(False)
            
    def set_view_callbacks(self):
        
        self.view.framescroller.scrollbar.valueChanged.connect(self.scroll)
        
    def set_model_callbacks(self):                        
        #self.model.index_changed.connect(self.image_index_update_callback)
        self.model.frame_index_changed.connect(self.image_index_update_callback)
        self.model.image_changed.connect(self.update_scrollbar)
        
    def image_index_update_callback(self, event_data=None):

        image = self.model[0].get_sitk_slice()
        fusion = self.model[1].get_sitk_slice()
        
        index = self.model.get_frame_index()

        self.view.framescroller.scrollbar.setValue(index)
        self.view.image_view.set_image_and_fusion(image, fusion)
         
    def scroll(self):
        self.model.set_frame_index(self.view.framescroller.scrollbar.value())
      
class SliceScrollController(ControllerBase):
    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, model=model, **kwargs)
        self.update_scrollbar()
        self.view.slicescroller.scrollbar.setValue(self.model.get_slice_index())

    def set_view_callbacks(self):
        
        self.view.slicescroller.scrollbar.valueChanged.connect(self.scroll)
        
    def set_model_callbacks(self):                        
        self.model.slice_changed.connect(self.image_index_update_callback)
        self.model.image_changed.connect(self.update_scrollbar)
        self.model.view_direction_changed.connect(self.update_scrollbar)
        
    def image_changed_callback(self):
        self.update_scrollbar()

    
    def update_scrollbar(self, index=None):        
        
        nslices = self.model.get_number_of_slices()
        
        if nslices <= 1:
            self.view.slicescroller.setVisible(False)            
        else:
            self.view.slicescroller.setVisible(True)            
            self.view.slicescroller.scrollbar.setMaximum(nslices-1)
            self.view.slicescroller.scrollbar.setValue(self.model.get_slice_index())
        
                            
    def scroll(self):
        self.model.set_slice_index(self.view.slicescroller.scrollbar.value())

        
    def image_index_update_callback(self, event_data=None):
        image = self.model[0].get_sitk_slice()
        fusion = self.model[1].get_sitk_slice()
        index = self.model.get_slice_index()

        self.view.slicescroller.scrollbar.setValue(index)
        self.view.image_view.set_image_and_fusion(image, fusion)
          
class ViewDirectionController(ControllerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_visible()
        
    def set_view_callbacks(self):        
        callback = self.set_view_direction
        self.view.orientation_buttons.button_clicked.connect(callback)
        
    def set_view_direction(self, view_direction):
        position = [*self.view.image_view.crosshair.get_position()]
       
        index = self.model[0].get_image_index(position)
        if len(index) < 3:
            raise
        self.model.set_view_direction(view_direction)
        
        direction = self.model.get_view_direction()
        
        if index is None:
            return

        
        if direction == SAGGITAL:
             slice_index = index[0]
             position = index[1:]                         
        elif direction == CORONAL:
             slice_index = index[1]
             position = [index[0], index[2]]                                      
        elif direction == AXIAL:
             slice_index = index[2]
             position = [index[0], self.model[0].get_image().GetSize()[1] - index[1]]
                         
        self.model.set_slice_index(slice_index)
        self.view.image_view.crosshair.set_position(position)
        
        # forces update of status text
        self.view.image_view.image_item.left_clicked.emit(position)
             
        
    def set_model_callbacks(self):  
        self.view.orientation_buttons.set_selected_button(self.model.get_view_direction())
        self.model.view_direction_changed.connect(self.update_view_direction)
        self.model.image_changed.connect(self.set_visible)
        
    def update_view_direction(self, view_direction):
        image_slice     = self.model[0].get_sitk_slice()
        fusion_slice    = self.model[1].get_sitk_slice()
        self.view.image_view.set_image_and_fusion(image_slice, fusion_slice)
    

    def set_visible(self):             
        visible = self.model[0].get_ndim() > 2                        
        self.view.orientation_buttons.setVisible(visible)
        if visible:
            view_direction = self.model.get_view_direction()
            self.view.orientation_buttons.set_selected_button(view_direction)

class SliceController(ControllerBase):
    _image_preset = None
    _index = None
    _image = None

    _mpl = None
    _view = None
    _view_direction = AXIAL

    def __init__(self, view=None, model=None, view_direction=AXIAL, preset_name=None,
                 presets=None):
        
   
        if model is None:
            model = SyncedImageSlicers(view_direction=view_direction)        
        if view is None:
            view = SliceViewerWidget()
        if presets is None:
            presets = PresetModel().load_from_disk(load_defaults=False)            
       
      
        self.presets = presets
        
        
        ControllerBase.__init__(self, model=model, view=view)
        
        
        self.style_controller.set_preset_by_name(preset_name)

        self.full_update_image()
        
        

    def create_subcontrollers(self):
    
        self.style_controller = StyleController(view=self.view,
                                                model=self.model,
                                                presets=self.presets)

        
        self.mouse = MouseOverPlotItemController(view=self.view,
                                                 model=self.model)
        
       
        
        self.slice_scroll_controller = SliceScrollController(view=self.view,
                                                             model=self.model)
        
        
        
        self.frame_scroll_controller = FrameScrollController(view=self.view,
                                                             model=self.model)
        
     
        
        self.view_direction_controller = ViewDirectionController(view=self.view,
                                                                 model=self.model)
   
        
    def set_model(self, model):
        self.model.unconnect(self)
        
        self.model = model
        self.set_model_callbacks()
        self.full_update_image()
        
    def full_update_image(self, event_data=None):
        self.refresh()        
        if self.model[0].get_image() is not None:
            pass
        self.view.image_view.plot_item.enableAutoRange()
    
    def refresh(self, event_data=None):
        image_slice     = self.model[0].get_sitk_slice()
        fusion_slice    = self.model[1].get_sitk_slice()
        
        self.view.image_view.set_image_and_fusion(image_slice, fusion_slice)

    def set_model_callbacks(self):
        self.model.image_changed.connect(self.full_update_image)

    def show_warning(self, msg):
        QMessageBox.warning(self.view, 'Simple Slice Browser', 
                             msg, QMessageBox.Ok)

class MouseOverPlotItemController(ControllerBase):
    EVENT_MOUSE_MOVE = 'event_mouse_move'
    _image_value = None
    _fusion_value = None
    _position = None
    
    _POSITION_PHYS = 'position'
    _POSITION_INDEX = 'position_index'
    _IMAGE_VALUE = 'image_value'
    _FUSION_VALUE = 'fusion_value'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.center_cross_hair()
    
    def set_view_callbacks(self):
        # plot_item = self.view.image_view.plot_item
        # self.mouse_poxy = pg.SignalProxy(plot_item.scene().sigMouseMoved, 
        #                                   rateLimit=60, slot=self.mouse_moved)
        self.view.image_view.image_item.left_clicked.connect(self.left_mouse_click)
    
    def set_model_callbacks(self):
        self.model[0].image_changed.connect(self.center_cross_hair)
        # self.view.image_view.crosshair.positionChanged.connect(self.mouse_click)
    #     self.model.view_direction_changed.connect(self.view_direction_changed)
        
    # def view_direction_changed(self, _):
    #     pos = self.view.image_view.crosshair.get_position()
    #     self.left_mouse_click(pos)
        
    def center_cross_hair(self):
        center = self.model[0].get_slice_center_index()
        self.view.image_view.crosshair.set_position(center)
        
    @staticmethod
    def smart_round(value, ndigits=4):
        if isinstance(value, (tuple, list)):
            return str([float(MouseOverPlotItemController.smart_round(ii)) for ii in value])
        elif value is None:
            return None
        
        if abs(value) == float('inf') or value == 0:
            return str(value) 
        
        
        # digits = int(ndigits - np.ceil(np.log10(abs(value))))
  
        if abs(value) < 10**ndigits and abs(value) > 10**-ndigits:
            value = round(value, ndigits)
            str_value = str(value)
        else:            
            str_value = f'{float(value):.{ndigits-1}e}'
        return str_value
    
    
    
    def left_mouse_click(self, pos):
        # self.model[0].set_slice_index([*pos])
        
        self.view.image_view.crosshair.set_position(pos)
        index = self.view.image_view.crosshair.get_position()
        
        image_data = self.get_image_data(index)
        self.set_statusbar(image_data)
        

    def mouse_moved(self, event):
        index = self.pos_index(event[0])   
            
        
        pos = self.model[0].transform_index_to_physical_point(index)    
        
        if pos is None:
            return
        
        self.update_position(event[0])
        
        self.view.status_label.setText(self.mouse_text)
        
    def get_image_data(self, index):

        pos_phys    = self.model[0].transform_index_to_physical_point(index)  
        im_val      = self.model[0].get_value_at_index(index)
        fusion_val  = self.model[1].get_value_at_index(index)
        im_index    = self.model[0].get_image_index(index)
        
        pos_phys    = self.smart_round(pos_phys, 1)
        im_val      = self.smart_round(im_val, 2)
        fusion_val  = self.smart_round(fusion_val, 2)
        if im_index is not None:
            im_index    = [int(ii) for ii in im_index]
        
        return {self._POSITION_PHYS: pos_phys,
                self._POSITION_INDEX: im_index,
                self._IMAGE_VALUE: im_val,
                self._FUSION_VALUE: fusion_val}

    def set_statusbar(self, image_data):
        text = ''
        if image_data[self._POSITION_PHYS] is not None:
            text += f'Mouse Position: {image_data[self._POSITION_PHYS]} [mm]'
        if image_data[self._POSITION_INDEX] is not None:
            text += f', {image_data[self._POSITION_INDEX]} [index]'
        if image_data[self._IMAGE_VALUE] is not None:
            text += f' | Image Value: {image_data[self._IMAGE_VALUE]}'
        if image_data[self._FUSION_VALUE] is not None:
            text +=  f' | Fusion Value: {image_data[self._FUSION_VALUE]}'
        self.view.status_label.setText(text)
        
        
    
    def pos_index(self, pos_view):
        plot_item = self.view.image_view.plot_item
        pos_index = plot_item.getViewBox().mapSceneToView(pos_view)
        return (pos_index.x(), pos_index.y())
                    
class MainController():
    def __init__(self, view=None, model=None, slice_controller=None,
                 preset_name=None, presets=None):
        
       
        if view is None:
            view = MainView()
        if model is None:
            model = SyncedImageSlicers()
        if slice_controller is None:
            slice_controller = SliceController(view=view.image_view,
                                               model=model, 
                                               preset_name=preset_name,
                                               presets=presets)
       
        
        self.view = view
        self.model = model
        
        
        
        self.slice_controller = slice_controller
        
        self.menubar = MenuBar(menubar=self.view.menuBar(),
                               presets=self.slice_controller.presets)
        
        self.set_callbacks()
        self.refresh()

    def image_menu_callback(self, menu_tree):
        

        if menu_tree[0]  == MenuBar.OPEN_FILE:
            self.load_image_from_file()
        elif menu_tree[0]  == MenuBar.LOAD_DICOM_FOLDER:
            self.load_image_from_dicom_folder()
        elif menu_tree[0]  == MenuBar.SAVE_FILE:
            self.save_image()
        elif menu_tree[0]  == MenuBar.LOAD_PET:
            self.load_pet_as_image()
       
            
    def fusion_menu_callback(self, menu_tree):
        if menu_tree[0] == MenuBar.OPEN_FILE:
            self.load_fusion_from_file()
        elif menu_tree[0] == MenuBar.LOAD_DICOM_FOLDER:
            self.load_fusion_from_dicom_folder()
        elif menu_tree[0] == MenuBar.REMOVE_FUSION:
            self.model.set_image(1, None)
        elif menu_tree[0] == MenuBar.SAVE_FILE:
            self.save_fusion()
        elif menu_tree[0] == MenuBar.LOAD_PET:
            self.load_pet_as_fusion()
    
    def export_menu_callback(self, menu_tree):
        if menu_tree[0] == MenuBar.MAKE_MOVIE:           
            movie_maker = MovieMaker(model=self.model,
                                     image_view=self.slice_controller.view.image_view)
            movie_maker.view.exec_()
        elif menu_tree[0] == MenuBar.MAKE_MOVIE_OF_FRAMES:
            movie_maker = MovieMaker(model=self.model,
                                     image_view=self.slice_controller.view.image_view, movie_type='frames')
            movie_maker.view.exec_()
        
    def set_callbacks(self):
        self.model.image_changed.connect(self.refresh)
        self.menubar.action_triggered.connect(self.menu_callback)
        
    def refresh(self):
        image_enabled = self.model.get_image(0) is not None
        fusion_enabled = self.model.get_image(1) is not None
        
        self.menubar.set_image_enabled(image_enabled)
        self.menubar.set_fusion_enabled(fusion_enabled)
        
        self.view.image_view.image_view.colorbar_image.setVisible(image_enabled)
        
        crosshair_action = self.menubar.get_action_by_name(MenuBar.SETTINGS, 
                                                           MenuBar.SHOW_CROSSHAIR)
        
        if not image_enabled:
            crosshair_action.setChecked(False)
            crosshair_action.setEnabled(False)
            self.view.image_view.image_view.crosshair.set_visible(False)
        else:
            crosshair_action.setEnabled(True)
            
        frame_action = self.menubar.get_action_by_name(MenuBar.EXPORT, 
                                                       MenuBar.MAKE_MOVIE_OF_FRAMES)
        
        slice_action = self.menubar.get_action_by_name(MenuBar.EXPORT, 
                                                       MenuBar.MAKE_MOVIE)
        
        if self.model[0].get_ndim() < 3:
            frame_action.setEnabled(False)
            slice_action.setEnabled(False)
        elif self.model[0].get_ndim() == 3:
            frame_action.setEnabled(False)
            slice_action.setEnabled(True)
        elif self.model[0].get_ndim() == 4 or self.model.get_ndim() == 4:
            frame_action.setEnabled(True)
            slice_action.setEnabled(True)
            
        
    def menu_callback(self, menu_tree):
        if menu_tree[0] == MenuBar.IMAGE:
            self.image_menu_callback(menu_tree[1:])
        elif menu_tree[0] == MenuBar.FUSION:
            self.fusion_menu_callback(menu_tree[1:])
        elif menu_tree[0] == MenuBar.PRESET_MENU:
            self.slice_controller.style_controller.set_preset_by_name(menu_tree[1])            
        elif menu_tree[0] == MenuBar.EXPORT:
            self.export_menu_callback(menu_tree[1:])
        elif menu_tree[0] == MenuBar.SETTINGS:
            self.settings_menu_callback(menu_tree[1])
            
    def settings_menu_callback(self, item_name):
        if item_name == MenuBar.COLORMAPS:
            self.select_available_colormaps()
        if item_name == MenuBar.SHOW_CROSSHAIR:            
            action = self.menubar.get_action_by_name(MenuBar.SETTINGS, 
                                                     MenuBar.SHOW_CROSSHAIR)
            visible = action.isChecked()
            self.view.image_view.image_view.crosshair.set_visible(visible)
            
    def select_available_colormaps(self):        
        dialog = AvailableColorScaleDialog(self.view)
        presets = self.slice_controller.presets
        def dialog_callback(result):
            if result == dialog.Accepted:
                presets.colormaps = dialog.to_list()
                
        cmaps = presets.colormaps
        dialog.from_list(cmaps)
        dialog.finished.connect(dialog_callback)
        dialog.exec_()
        
        
    def load_pet_as_image(self):
        dlg = LoadPETController(parent=self.view)
        dlg.view.exec_()
        if isinstance(dlg.image, sitk.Image):

            self.model.set_image(0, dlg.image)
        del dlg
    
    def load_pet_as_fusion(self):
        dlg = LoadPETController()
        dlg.view.exec_()
        if isinstance(dlg.image, sitk.Image):
            self.model.set_image(1, dlg.image)
        del dlg
            
    def _write_image(self, image):
        filename = self.get_file_to_write()
        if filename:
            try:
                sitk.WriteImage(image, filename)
            except:
                self.file_write_warning(filename)
                
    def file_write_warning(self, file):
        warning_txt = f'Cannot write file {file}'
        dlg = QMessageBox(self.view, QMessageBox.Warning, 'Warning!', warning_txt)
        dlg.exec()
        print(warning_txt)
    
    def get_file_to_write(self):
        extension = "NIFTY (*.nii);; NIFTY (*.nia);; NIFTY (*.nii.gz);; NIFTY (*.img.gz )"
        file = QFileDialog.getSaveFileName(self.view, 'Select a file:', 
                                           'image.nii',
                                            filter=extension)
        return file[0]
                
    def save_image(self):
        self._write_image(self.model[0].get_image())
        
    def save_fusion(self):
        self._write_image(self.model[1].get_image())

    def read_dicom(self):
        folder = self.get_open_folder()
        image = None
        if folder:
            try:
                image = sitk_tools.read_folder(folder, recursive=True, 
                                              frame_tag=None)
            except:
                self.show_warning(f'Failed to load Dicom folder {folder}')

        return image
        
    def get_open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self.view, "Select Image File", "", SUPPORTED_FILES)
            
        return file_name
    
    def get_open_folder(self, msg="Select Folder"):
        folder_name = QFileDialog.getExistingDirectory(self.view, msg)
        return folder_name
                            
    def read_image(self):
        file_name = self.get_open_file()
        image = None
        if file_name:
            try:
                image = sitk.ReadImage(file_name)
            except:
                self.show_warning(f'Could not open file {file_name}')
        return image
    
    def load_image_from_dicom_folder(self):
        image = self.read_dicom()
        if image is not None:
            self.model.set_image(0, image)
    
    def load_fusion_from_dicom_folder(self):
        image = self.read_dicom()
        if image is not None:
            self.model.set_image(1, image)                   
    
    def load_image_from_file(self):
        image = self.read_image()
        if image is not None:
            self.model.set_image(0, image)
        
    def load_fusion_from_file(self):
        image = self.read_image()
        if image is not None:
            self.model.set_image(1, image)            
        

def safe_load_image(image):
    if isinstance(image, sitk.Image) or image is None:
        return image
    elif isinstance(image, str) and not os.path.exists(image):
        raise IOError(f'File not found: {image}')
    elif os.path.isfile(image):
        try:
            image = sitk.ReadImage(image)
        except:
            try:
                image = sitk_tools.read_file(image)
            except:
                raise IOError(f'Could not read {image}!')
    elif os.path.isdir(image):
        try:
            image = sitk_tools.read_folder(image)
        except:
            raise IOError(f'Could not read folder as DICOM: {image}')
    return image
        
    
def display(image=None, 
            fusion=None, 
            view_direction=None, 
            preset_name=None,
            new_qapp=True):
    
    image = safe_load_image(image)
    fusion = safe_load_image(fusion)
    
    if new_qapp:
        app = QApplication([])

        color = app.palette().color(app.palette().Background)
        pg.setConfigOption('background', color)
        pg.setConfigOption('foreground', 'k')
    
    
    model = SyncedImageSlicers(images=[image, fusion],
                               view_direction=view_direction)
    
    controller = MainController(model=model, preset_name=preset_name)
        
    controller.view.show()
    
    if new_qapp:
        app.exec()
    
    return controller

    
if __name__ == "__main__": 
    import sys
    image = None
    fusion = None
    if len(sys.argv) > 1:
        image = sys.argv[1]
    if len(sys.argv) > 2:
        fusion = sys.argv[2]
    controller = display(image=image, fusion=fusion)
    