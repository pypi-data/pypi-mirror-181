from PyQt5.Qt import QCursor

from simple_slice_viewer.controller_base import ControllerBase, StyleControllerBase
from simple_slice_viewer.preset_model import ColorScale, ImagePreset,  PresetModel
from simple_slice_viewer.preset_view import ImageFusionPresetDialog, ImagePresetDialog, AvailableColorScaleDialog
from simple_slice_viewer.menus import ColorBarContextMenu

        
    
class ImageStyleController(StyleControllerBase):                                    
    _preset = None
    _alpha = None
    def __init__(self, *args, alpha_slider=None, **kwargs):
        self.alpha_slider = alpha_slider
        super().__init__(*args, **kwargs)
    
    def model_update_image_callback(self):
        super().model_update_image_callback()
        preset = self.get_preset()
        self.set_preset_in_view(preset)
        
    
    def set_view_callbacks(self):
        super().set_view_callbacks()
        if self.alpha_slider is not None:
            self.alpha_slider.scrollbar.valueChanged.connect(self.view.set_alpha)
    
    def set_alpha(self, alpha):           
        if self._alpha != alpha:           
            self._alpha = alpha
            if self.alpha_slider is not None:
                self.alpha_slider.scrollbar.setValue(int(round(alpha)))
            self.view.set_alpha(alpha)
            
    def get_alpha_from_view(self):
        return self.view.alpha_slider.scrollbar.value()
        
    def set_preset_in_view(self, preset):    
        self._preset = preset

        self.set_colorscale_in_view(preset.colorscale)
        self.set_colormap_in_view(preset.colormap)
        self.set_alpha(preset.alpha)
                        
    def get_preset(self):
        if self._preset is None:
            self._preset = self.presets[0]
        return self._preset
                                  
    def set_colorscale_in_view(self, colorscale):
        if colorscale is None:
            colorscale = self.colorscales[0]
        elif isinstance(colorscale, ColorScale):
            pass
        else:
            raise TypeError(f'type {colorscale}')
    
        clim = colorscale.get_clim(clim_range=self.model.get_clim())
        self.view.setLevels(clim)
    
    def set_colormap_in_view(self, colormap):

        self.view.setColorMap(ImagePreset.get_pg_colormap(colormap))        

class StyleController(StyleControllerBase):
    _preset = None
    def __init__(self, model=None, view=None, presets=None,
                 enabled=True):
        self.enabled = enabled

        self.presets = presets
        
        super().__init__(model=model, 
                         view=view, 
                         presets=presets)
        
        self.set_visibility_fusion_colorbar()
        self.set_right_click()
        
    def set_preset_by_name(self, preset_name):

        preset = self.presets.image_fusion_presets.get_item_by_name(preset_name)
        if preset is None:
            return

        self.set_preset(preset)

    def get_preset(self):
        if self._preset is None:
            self._preset = self.presets.image_fusion_presets[0]
        return self._preset
    
    def set_preset(self, preset):
        if preset is None:
            return 
        self._preset = preset
        image_preset = self.presets.image_presets.get_item_by_name(preset.image_preset)

        self.image_colormap_controller.set_preset_in_view(image_preset)
        
        fusion_preset = self.presets.fusion_presets.get_item_by_name(preset.fusion_preset)
        self.fusion_colormap_controller.set_preset_in_view(fusion_preset)
       
            
    def set_right_click(self):
        view = self.view.image_view
        callback = lambda contr=self.image_colormap_controller:\
            self.show_colorbar_menu(contr, label='Image')
            
        view.colorbar_image.right_clicked.connect(callback)
        
        callback = lambda contr=self.fusion_colormap_controller:\
            self.show_colorbar_menu(contr, label='Fusion')

        view.colorbar_fusion.right_clicked.connect(callback)
        
        view.image_item.right_clicked.connect(self.show_preset_menu)
        
    def show_preset_menu(self):   
        if self.model.get_image(1) is None:
            return
        
        self.preset_menu = ColorBarContextMenu('Image Preset', 
                                               label = 'Image Fusion Preset',
                                               presets = self.presets.image_fusion_presets, 
                                               cmaps=None)
        preset = self.get_preset()
        
        def show_preset_widget():
            
                
            view = ImageFusionPresetDialog(parent=self.view)
            view.image_preset_combo.addItems(self.presets.image_presets.get_names())
            view.fusion_preset_combo.addItems(self.presets.fusion_presets.get_names())
            view.image_preset_combo.setCurrentText(preset.image_preset)
            view.fusion_preset_combo.setCurrentText(preset.fusion_preset)
            view.preset_name.setText(preset.name)
            
            def set_preset():
                if view.result() == view.Accepted:
                    new_preset = view.get_preset()
                    presets = self.presets.image_fusion_presets
                    listed_preset = presets.get_item_by_name(new_preset.name)
                    listed_preset.update(**dict(new_preset))
                    self.set_preset(listed_preset)
            
            def new_preset():
                presets = self.presets.image_fusion_presets
                presets.add()
                view.set_preset(presets[-1])
            
            def delete_preset():
                preset = view.get_preset()
                presets = self.presets.image_fusion_presets
                listed_preset = presets.get_item_by_name(preset.name)
                
                index = presets.item_list.index(listed_preset)
                if len(presets)>1:
                    presets.delete(index)
                    index = max(index-1, 0)
                    view.set_preset(presets[index])
                
            callback = self.presets.save_to_disk
            self.preset_menu.save_preset_action.triggered.connect(callback)
            
            view.finished.connect(set_preset)
            view.new_button.clicked.connect(new_preset)
            view.delete_button.clicked.connect(delete_preset)
            view.exec_()
                                            
        
            
        cback = lambda tree: self.set_preset_by_name(tree[1])
        self.preset_menu.preset_menu.action_triggered.connect(cback)
        
        self.preset_menu.colorscale_action.triggered.connect(show_preset_widget)

        
        self.preset_menu.exec_(QCursor().pos())
    
    def show_colorbar_menu(self, preset_controller, label=''):        
        def set_preset(menu_response):
            preset_type, preset_name = menu_response
           
            if 'Image' in preset_type:
                preset = self.presets.image_presets.get_item_by_name(preset_name)
            else:
                preset = self.presets.fusion_presets.get_item_by_name(preset_name)
                
            
          
            preset_controller.set_preset_in_view(preset)
        
        def show_colorscale_widget():
            contr = ImagePresetController(model=self.presets, parent=self.view)
       
            def new_preset_event():

                preset_controller.presets.add()
                preset = preset_controller.presets[-1]
                contr.set_preset(preset)
                
           
      
            def delete_preset_event():
                if len(preset_controller.presets) == 1:
                    return
                
                
                preset_name = contr.view.preset_name.text()
                if 'Image' in label:
                    used = self.presets.get_used_imagepreset_names()
                else:
                    used = self.presets.get_used_fusionpreset_names()
                
                if preset_name in used:
                    print(f'Preset {preset_name} is in use and cannot be deleted!')
                    return
                
                preset = preset_controller.presets.get_item_by_name(preset_name)
                
                
                index = preset_controller.presets.item_list.index(preset)
                
                if index == 0:
                    new_index = 0
                else:
                    new_index = index - 1
                    
                preset_controller.presets.delete(index)
                
                preset = preset_controller.presets[new_index]
                
                contr.set_preset(preset)
                preset_controller.set_preset_in_view(preset)

                
                
            
            contr.view.new_preset_event.connect(new_preset_event)
            contr.view.delete_preset_event.connect(delete_preset_event)
            
            new_preset = contr.show_dialog(preset_controller.get_preset())
            
            self._new_preset = new_preset
            
            if new_preset is None:
                return
            
            listed_preset = preset_controller.presets.get_item_by_name(new_preset.name)
       
   
            listed_preset.update(colorscale=new_preset.colorscale,
                                alpha=new_preset.alpha,
                                colormap=new_preset.colormap)
            
            preset_controller.set_preset_in_view(listed_preset)
            
                
        
            
        
        cmaps = self.presets.colormaps
        
        if 'Image' in label:
            presets = self.presets.image_presets
        else:
            presets = self.presets.fusion_presets
        
        preset_controller.context_menu = ColorBarContextMenu(presets=presets,
                                                            label=label,
                                                            cmaps=cmaps)
        cback = preset_controller.set_colormap_in_view
        preset_controller.context_menu.cmap_menu.action_triggered.connect(cback)
        
        callback = set_preset
        preset_controller.context_menu.preset_menu.action_triggered.connect(callback)
        
        callback = lambda _: show_colorscale_widget()
        preset_controller.context_menu.colorscale_action.triggered.connect(callback)
        
        # callback = lambda _, contr=preset_controller: self.show_save_preset_dialog(contr)
        # preset_controller.context_menu.save_preset_action.triggered.connect(callback)
        
        callback = self.presets.save_to_disk
        preset_controller.context_menu.save_preset_action.triggered.connect(callback)
        
        
        preset_controller.context_menu.exec_(QCursor().pos())
        
   
        


        
    def model_update_image_callback(self):
        super().model_update_image_callback()    
        self.set_visibility_fusion_colorbar()
        # self.set_enabled_context_menus() # 2DO
        
    def set_visibility_fusion_colorbar(self):
        visible = self.model[1].get_image() is not None
        self.view.image_view.colorbar_fusion.setVisible(visible)
        self.view.image_view.fusion_item.setVisible(visible)
        self.view.alpha_slider.setVisible(visible)
        
    def create_subcontrollers(self):
        # self.alpha_controller = AlphaController(presets=self.presets.fusion_presets,
        #                                         model=self.model,
        #                                         view=self.view)
        
        contr = ImageStyleController(view=self.view.image_view.colorbar_image,
                                     model=self.model[0],
                                     presets=self.presets.image_presets)
                                     
                                    
                                    
        
        self.image_colormap_controller = contr
                                     

        contr = ImageStyleController(view=self.view.image_view.colorbar_fusion,
                                      model=self.model[1],
                                      presets=self.presets.fusion_presets,
                                      alpha_slider=self.view.alpha_slider)
                                     
                                     
        
        self.fusion_colormap_controller = contr 
        
    
class ImagePresetController(ControllerBase):
    _preset = None
    
    
    def __init__(self, view=None, model=None, parent=None):
        if view is None:
            view = ImagePresetDialog(parent=parent)
        if model is None:
            model = PresetModel.load_from_disk(load_defaults=True)

    
        super().__init__(model=model, view=view)

        self.update_colormap_combo()

    def get_preset(self):
        scale = ColorScale(scale_type=self.view.get_scale_type(),
                            scale=self.view.get_scale())
        preset = ImagePreset(name=self.view.preset_name.text(),
                            colormap = self.view.get_colormap(),
                            colorscale = scale,
                            alpha=self.view.get_alpha())
        return preset
        
    # def get_preset(self):
    #     if self._preset is None:
    #         self._preset = self.presets[0]        
    #     return self._preset
    
    def set_preset(self, preset=None):

        self.view.preset_name.setText(preset.name)        
        self.view.set_colorscale(preset.colorscale)
        self.view.set_colormap(preset.colormap)
        self.view.set_alpha(preset.alpha)
        
    def refresh(self):
        self.set_preset()
        
    def show_dialog(self, preset=None):
        if preset is None:
            preset = self.model.image_presets[0]
                    
        self.set_preset(preset)
        
        def dialog_finished():
            if self.view.result() == self.view.Accepted:
                self._new_preset = self.get_preset()
            else:
                self._new_preset = None
                
            
        self.view.finished.connect(dialog_finished)
        self.view.exec_()
        return self._new_preset
        
    def set_view_callbacks(self):
        self.view.colormap_button.clicked.connect(self.showcolormap_dialog)
        self.view.new_button.clicked.connect(self.view.new_preset_event.emit)
        self.view.delete_button.clicked.connect(self.view.delete_preset_event.emit)
        
    def showcolormap_dialog(self):
        dlg = AvailableColorScaleDialog()
        dlg.from_list(self.model.colormaps)
        
        def dialog_finished():
            if dlg.result() == dlg.Accepted:        
                self.model.colormaps = dlg.to_list()
                if len(self.model.colormaps) == 0:
                    self.model.colormaps = ['gray']
                self.update_colormap_combo()

  
        dlg.finished.connect(dialog_finished)
        dlg.exec_()
        
       
        
    def update_colormap_combo(self):
        current_text = self.view.colormap_combo.currentText()
        self.view.colormap_combo.clear()
        self.view.colormap_combo.addItems(self.model.colormaps)
        
        if current_text in self.model.colormaps:
            self.view.colormap_combo.setCurrentText(current_text)
        else:
            self.view.colormap_combo.setCurrentIndex(0)
            
        