class ControllerBase():
    def __init__(self, model=None, view=None):        
        self.model = model
        self.view = view
        
        self.create_subcontrollers()
        self.set_model_callbacks()
        self.set_view_callbacks()
        
    def create_subcontrollers(self):
        pass
        
    def set_model_callbacks(self):
        pass
        
    def set_view_callbacks(self):
        pass
    

class StyleControllerBase(ControllerBase):
    _preset_name = None
    
    def __init__(self, model=None, view=None, presets=None):
        
        self.presets = presets
        ControllerBase.__init__(self, model=model, view=view)
        self.set_preset_callbacks()
        self.refresh()

    def set_model_callbacks(self):
        if self.model is not None:
            self.model.image_changed.connect(self.model_update_image_callback)
            self.model.slice_changed.connect(self.model_update_index_callback)
   
    def model_update_index_callback(self):
        # new slice selected
        pass
    
    def model_update_image_callback(self):
        # triggered when model loads new image
        # force update of preset to display new image correctly        
        self.preset_update_callback()
        
    def set_preset_callbacks(self):
        pass
        # self.presets.dataChanged.connect(self.preset_update_callback)
        # self.presets.presetChanged.connect(self.set_preset_by_name)
        
    def preset_update_callback(self):
        pass
        # triggered when values of preset change
        # self.refresh()

    def set_preset_by_name(self, preset_name):
        # triggered when new preset is selected
        preset = self.presets.get_item_by_name(preset_name)

        self.set_preset(preset)
    
    def set_preset(self, preset):
        pass
    
    def get_preset_names(self):
        return [preset.name for preset in self.presets]
    
    def get_active_preset(self):
        if self._preset is None:
            self._preset = self.presets[0]
        return self._preset
        pass
        # if self._preset_name is None or self._preset_name not in self.get_preset_names():
        #     self._preset_name = self.presets[0].name
        # return self.presets.get_item_by_name(self._preset_name)
        
    def refresh(self):
        pass