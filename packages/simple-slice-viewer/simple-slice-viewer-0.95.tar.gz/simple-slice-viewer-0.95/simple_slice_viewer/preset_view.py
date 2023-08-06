from simple_slice_viewer.view import WidgetBase
from PyQt5.QtWidgets import QScrollBar, QLabel, QComboBox, QLineEdit, QDoubleSpinBox, QRadioButton, QApplication, QPushButton, QCheckBox, QDialog, QGridLayout
from PyQt5.QtCore import  pyqtSignal
from simple_slice_viewer.preset_model import ColorScale, ImagePreset, ImageFusionPreset, PresetModel
from PyQt5.QtCore import Qt

PERCENTAGE_MAX_OPTIONS = ['0%', '1%', '5%', '10%', '30%', '50%', '70%', '90%', '95%', '99%', '100%']

class QDialogBase(QDialog):
    _layout = None
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.create_widgets()
        self.create_layout()
        self.create_bottom_layout()
        self.set_callbacks()
        self.setLayout(self.layout)
        self.set_widgets()
        
    def create_widgets(self):
        pass
    
    def create_layout(self):
        pass
    
    def create_bottom_layout(self):
        pass
    
    def set_callbacks(self):
        pass
    
    def set_widgets(self):
        pass

    @property
    def layout(self):
        if self._layout is None:
            self._layout = self._get_layout_object()
        return self._layout
    
    @layout.setter
    def layout(self, layout):
        self._layout = layout
        
    
    def _get_layout_object(self):
        return QGridLayout()
    
    @staticmethod
    def set_combo_to_text(combo, text):
        combo.setCurrentIndex(combo.findText(str(text)))
        
class PresetSaveDialog(QDialogBase):
    def create_widgets(self):
        self.existing_radio = QRadioButton('Overwrite Existing Preset')
        self.existing_combo = QComboBox()
        
        self.new_radio = QRadioButton('Create New Preset')
        self.new_label = QLabel('Preset Name: ')
        self.new_input = QLineEdit()
        
        self.apply_button = QPushButton('Save')
        # self.cancel_button = QPushButton('Cancel')
        
    def set_widgets(self):
        self.new_radio.setChecked(True)
        
    def set_callbacks(self):
        # self.apply_button.clicked.connect(self.accept)
        # self.cancel_button.clicked.connect(self.reject)
        
        self.existing_radio.toggled.connect(self.toggle)
        self.new_radio.toggled.connect(self.toggle)
        
    def toggle(self):
        new_checked = self.new_radio.isChecked()
        existing_checked = self.existing_radio.isChecked()
        
        self.new_label.setEnabled(new_checked)
        self.new_input.setEnabled(new_checked)
        
        self.existing_combo.setEnabled(existing_checked)
        
    def get_preset_name(self):
        if self.new_radio.isChecked():
            return self.new_input.text()
        elif self.existing_radio.isChecked():
            return self.existing_combo.currentText()
        
    def set_existing_presets(self, presets):
        self.existing_combo.addItems(presets)
        self.existing_combo.setCurrentIndex(0)

    def create_layout(self):
        row = 0
        self.layout.addWidget(self.existing_radio, row, 0)

        row += 1
        
        self.layout.addWidget(self.existing_combo, row, 0)
        
        row += 1
        
        self.layout.addWidget(self.new_radio, row, 0)
                              
        row += 1
        
        self.layout.addWidget(self.new_label, row, 0)
        
        row += 1
        
        self.layout.addWidget(self.new_input, row, 0)
        
        row += 1
       
        self.layout.addWidget(self.apply_button, row, 0)
    
        # row += 1
        
        # self.layout.addWidget(self.cancel_button, row, 0)

class AvailableColorScaleDialog(QDialogBase):
    ncols = 5
    def create_widgets(self):
        cmaps = ImagePreset.get_available_colormaps()
        self.checkboxes = {}
        for cmap in cmaps:
            self.checkboxes[cmap] = QCheckBox(cmap)
            
        self.apply_button = QPushButton('Apply')
        self.cancel_button = QPushButton('Cancel')
        self.setWindowTitle('Available Colormaps')
    
    def from_list(self, cmaps):
        for box in self.checkboxes.values():
            box.setChecked(False)
            
        for cmap in cmaps:
            # if cmap not in self.checkboxes.keys():
            #     raise KeyError(f'{cmap} not a valid colormap!')            
            self.checkboxes[cmap].setChecked(True)
            
    def to_list(self):
        cmaps = []
        for cmap, box in self.checkboxes.items():
            if box.isChecked():
                cmaps += [cmap]
        return cmaps
    
    def set_callbacks(self):
        self.apply_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
    
    def create_layout(self):
        col = 0
        row = 0
        for cbox in self.checkboxes.values():
            self.layout.addWidget(cbox, row, col)
            col += 1
            if col == self.ncols:
                row += 1
                col = 0
                
        row += 1
        
        self.layout.addWidget(self.apply_button, row, 0, 1, self.ncols)
        
        row += 1
        
        self.layout.addWidget(self.cancel_button, row, 0, 1, self.ncols)
                
        
class RadioButtonGroup(WidgetBase):
    def __init__(self, *args, ncols=None):
        self.ncols = ncols
        self.title = args[0]
        self.button_names = args[1:]
        super().__init__()

    def create_widgets(self):
        self.radio_buttons = []
        self.title_label = QLabel(self.title)
        for name in self.button_names:
      
            self.radio_buttons += [QRadioButton(name)]
        
    def create_layout(self):
        self.layout.addWidget(self.title_label, 0, 0)
        if self.ncols is None:
            self.ncols = 1
            
        col = 0
        for index, button in enumerate(self.radio_buttons):
            
            row = int(index/self.ncols)        
   
            self.layout.addWidget(button, row + 1, col)
            col += 1
            if col == self.ncols:
                col = 0
            
    def setValue(self, value):
        if not isinstance(value, str):
            value = int(value)
            value = str(value)
        if value[-1] != '%':
            value += '%'
        if value not in self.button_names:
            msg = f'{value} not in {self.button_names}!'
            raise ValueError(msg)
        for name, radio in zip(self.button_names, self.radio_buttons):
            if name == value:
                radio.setChecked(True)
    
    def value(self):
        for index, radio in enumerate(self.radio_buttons):
            if radio.isChecked():
                str_value = self.button_names[index]
                value = float(str_value.replace('%', ''))
                return value
            
            
class MinMaxRangeWidget(WidgetBase):
    VALUES = PERCENTAGE_MAX_OPTIONS
    
    def create_widgets(self):
        self.min_radios = RadioButtonGroup('Minimum', *self.VALUES, ncols=3)
        self.max_radios = RadioButtonGroup('Maximum', *self.VALUES, ncols=3)
        
    def create_layout(self):
        row = 0
        
        self.layout.addWidget(self.min_radios, row, 0)
        self.layout.addWidget(self.max_radios, row, 1)
        
    def setValues(self, values):
        self.min_radios.setValue(values[0])
        self.max_radios.setValue(values[1])
        
    def values(self):
        return [self.min_radios.value(), self.max_radios.value()]

        
        
class FixedScaleWidget(WidgetBase):
    def __init__(self, *labels):
        self.labels = labels
        super().__init__()
        
    def create_widgets(self):
        self.qlabels = {}
        self.qvalues = {}
        for label in self.labels:
            self.qlabels[label] = QLabel(label)
            self.qvalues[label] = QDoubleSpinBox()
            
    def create_layout(self):
        for row, (qlabel, qvalue) in enumerate(zip(self.qlabels.values(), 
                                                   self.qvalues.values())):
            self.layout.addWidget(qlabel, row, 0)
            self.layout.addWidget(qvalue, row, 1)
    
    def setMinimum(self, value):
        for qvalue in self.qvalues.values():
            qvalue.setMinimum(value)
    
    def setMaximum(self, value):
        for qvalue in self.qvalues.values():
            qvalue.setMaximum(value)
    
    def setRange(self, minval, maxval):
        for qvalue in self.qvalues.values():
            qvalue.setRange(minval, maxval)
            
    def setValues(self, values):
        for value, qvalue in zip(values, self.qvalues.values()):
            qvalue.setValue(value)

    def values(self):
        return [qvalue.value() for qvalue in self.qvalues.values()]

class ImageFusionPresetDialog(QDialogBase):

    
    def create_widgets(self):
        self.preset_label = QLabel('Preset')
        self.preset_name = QLabel('Preset')
        self.image_preset_label = QLabel('Image Preset')
        self.image_preset_combo = QComboBox()
        self.fusion_preset_label = QLabel('Fusion Preset')
        self.fusion_preset_combo = QComboBox()
        
        self.apply_button = QPushButton('Apply')
        self.cancel_button = QPushButton('Cancel')
        self.new_button = QPushButton('New Preset')
        self.delete_button = QPushButton('Delete Preset')
    def create_layout(self):
        row = 0
        
        self.layout.addWidget(self.preset_label, row, 0)
        self.layout.addWidget(self.preset_name, row, 1)
        row += 1
        
        self.layout.addWidget(self.image_preset_label, row, 0)
        self.layout.addWidget(self.image_preset_combo, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.fusion_preset_label, row, 0)
        self.layout.addWidget(self.fusion_preset_combo, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.new_button, row, 0)
        self.layout.addWidget(self.delete_button, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.apply_button, row, 0)
        
        # row += 1
        
        self.layout.addWidget(self.cancel_button, row, 1)
    
    def set_callbacks(self):
        
        self.apply_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
    def set_widgets(self):
        self.setWindowTitle('Image Fusion Presets')
    
    def get_preset(self):
        preset = ImageFusionPreset(name=self.preset_name.text(),
                                  image_preset=self.image_preset_combo.currentText(),
                                  fusion_preset=self.fusion_preset_combo.currentText())
        return preset
    
    def set_preset(self, preset):
        self.preset_name.setText(preset.name)
        self.image_preset_combo.setCurrentText(preset.image_preset)
        self.fusion_preset_combo.setCurrentText(preset.fusion_preset)
    
    
        
class ImagePresetDialog(QDialogBase):
    new_preset_event = pyqtSignal()
    delete_preset_event = pyqtSignal()
    def create_widgets(self):
        
        super().create_widgets()
        
        self.preset_label   = QLabel('Preset Name')
        self.preset_name    = QLabel('Name')
        
        self.type_minmax    = QRadioButton('Relative to Maximum')
        self.type_wl        = QRadioButton('Window - Level')
        self.type_fixed     = QRadioButton('Fixed Value')
        
        
        self.widget_fixed   = FixedScaleWidget('Minimum', 'Maximum')
        self.widget_fixed.setRange(-float('inf'), float('inf'))
        
        self.widget_wl   = FixedScaleWidget('Window', 'Level')
        self.widget_wl.setRange(-float('inf'), float('inf'))
        
        self.widget_minmax =  MinMaxRangeWidget()
        
        # self.save_widget = PresetSaveDialog()
        
        self.alpha_slider = QScrollBar(Qt.Horizontal)
        self.alpha_label = QLabel('0%')
        
        self.colormap_label = QLabel('Colormap')
        
        self.colormap_combo = QComboBox()
        self.colormap_button = QPushButton('Add colormaps')
        self.apply_button = QPushButton('Apply')
        self.cancel_button = QPushButton('Cancel')
        self.new_button = QPushButton('New Preset')
        self.delete_button = QPushButton('Delete Preset')
        self.setWindowTitle('Image Preset')
        
    def create_layout(self):
        super().create_layout()
       
        row = self.layout.rowCount() + 1
        
        self.layout.addWidget(self.preset_label, row, 0)
        
        self.layout.addWidget(self.preset_name, row, 1)
        
        row += 1
               
        self.layout.addWidget(self.type_wl, row, 0, 1, 2)
                
        row += 1
        
        self.layout.addWidget(self.widget_wl, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.type_fixed, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.widget_fixed, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.type_minmax, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.widget_minmax, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.alpha_label, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.alpha_slider, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.colormap_label, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.colormap_combo, row, 0)
        
        # row += 1
        
        self.layout.addWidget(self.colormap_button, row, 1)
        # self.layout.addWidget(self.save_widget, row, 0)
        
        row += 1
        
        self.layout.addWidget(self.new_button, row, 0)
        self.layout.addWidget(self.delete_button, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.apply_button, row, 0, 1, 1)
        
        # row += 1
        
        self.layout.addWidget(self.cancel_button, row, 1, 1, 1)
    

    def get_alpha(self):
        return self.alpha_slider.value()
    
    def set_alpha(self, alpha):
        self.alpha_slider.setValue(alpha)
        
    def update_alpha_label(self, value):
        self.alpha_label.setText(f'Alpha: { int(value)}%')
        
    def showsave_diaolog(self):
        dlg = PresetSaveDialog()
        dlg.exec_()
        
    def set_widgets(self):
        self.colormap_combo.addItems(ImagePreset.get_available_colormaps())
        self.alpha_slider.setMinimum(0)
        self.alpha_slider.setMaximum(100)
  
    
    def set_colormap(self, colormap):
        self.colormap_combo.setCurrentText(colormap)
        
    def get_colormap(self):
        return self.colormap_combo.currentText()
        
    def _get_scale_types(self):
        return [ColorScale.WINDOW_LEVEL, ColorScale.FIXED, 
                ColorScale.RELATIVE_MIN_MAX]
    
    def _get_radios(self):
        return [self.type_wl, self.type_fixed, self.type_minmax]
    
    def _get_widgets(self):
        return [self.widget_wl, self.widget_fixed, self.widget_minmax]

    def set_callbacks(self):        
        super().set_callbacks()        
        
        # self.save_button.clicked.connect(self.showsave_diaolog)
        self.type_wl.toggled.connect(self.toggle)
        self.type_minmax.toggled.connect(self.toggle)
        self.type_fixed.toggled.connect(self.toggle)
        
        self.apply_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        self.alpha_slider.valueChanged.connect(self.update_alpha_label)
                
    def toggle(self, *args, **kwargs):
        for radio, widget in zip(self._get_radios(), self._get_widgets()):
            enabled = radio.isChecked()         
            widget.setEnabled(enabled)
            
    def from_model(self, model):
   
        self.set_scale_type(model.scale_type)
        self.set_scale(model.scale)
    
    def to_model(self):
        model = ColorScale(scale_type=self.get_scale_type(),
                           scale=self.get_scale())
        return model
        
    def set_colorscale(self, colorscale):

        self.set_scale_type(colorscale.scale_type)
        self.set_scale(colorscale.scale)
        
    
    
    def get_scale(self):
        for radio, widget in zip(self._get_radios(), self._get_widgets()):
            if radio.isChecked():
                return widget.values()
            
    def set_scale(self, scale):

        for radio, widget in zip(self._get_radios(), self._get_widgets()):
            if radio.isChecked():
                return widget.setValues(scale)
            
    def get_scale_type(self):
        for stype, radio in zip(self._get_scale_types(), self._get_radios()):
            if radio.isChecked():
                return stype
    
    def set_scale_type(self, scale_type):
 
        for stype, radio in zip(self._get_scale_types(), self._get_radios()):
            if stype == scale_type:
                radio.setChecked(True)

                
  
        
    
        

        
     

if __name__ == "__main__":
    #import qdarkstyle
    from simple_slice_viewer.preset_model import PresetModel
    presets = PresetModel().load_from_disk(load_defaults=True)
    
    app = QApplication([])
    view = ImageFusionPresetDialog()
    view.image_preset_combo.addItems(presets.image_presets.get_names())
    view.fusion_preset_combo.addItems(presets.image_presets.get_names())
    view.set_preset(presets.image_fusion_presets[0])
    view.exec_()
    # contr = ImageFuPresetController()
    # contr.show_dialog(presets.image_presets[0])
    # view.save_widget.set_existing_presets([preset.name for preset in presets.image_presets])
#     view.save_widget.new_input.setText(presets.image_presets.get_new_name())
    # view.from_model(app.c)
    # view.from_list(presets.colormaps)
    

    
    #model=StyleModel().load_from_disk()
    #controller = St