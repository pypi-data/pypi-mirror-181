from simple_slice_viewer.view import WidgetBase
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableView, QLabel, QFileDialog, QLineEdit, QDateEdit, QTimeEdit, QDoubleSpinBox, QRadioButton, QApplication, QPushButton, QCheckBox
from PyQt5 import QtCore
from simple_slice_viewer.controller_base import ControllerBase
from simple_slice_viewer.preset_view import QDialogBase
from datetime import datetime, time, date
import sitk_tools
import SimpleITK as sitk
import os
import pydicom
import numpy as np
import pandas as pd
import qtawesome as qta

def set_widget(widget, value, default_value=None):
    if isinstance(widget, QDoubleSpinBox):
        if value is None:
            value = default_value if default_value else 0
        widget.setValue(value)
    elif isinstance(widget, QTimeEdit):
        if value is None:
            value = default_value if default_value else time(0, 0, 0)
        widget.setTime(value)
    elif isinstance(widget, QDateEdit):
        if value is None:
            value = default_value if default_value else date(2001, 1, 1)
        widget.setDate(value)
        
def get_widget(widget):
    if isinstance(widget, QDoubleSpinBox):
        value = widget.value()
    elif isinstance(widget, QTimeEdit):
        value = widget.time().toPyTime()
    elif isinstance(widget, QDateEdit):
        value = widget.date().toPyDate()
    return value
    

class FrameTimeWidget(QDialogBase):
    def create_widgets(self):
        self.table = QTableView(self)
        self.close_button = QPushButton('Close')
        self.export_button = QPushButton('Export To Excel')
        
    def create_layout(self):
        row = 0
        
        self.layout.addWidget(self.table, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.export_button,   row, 0)
        self.layout.addWidget(self.close_button,    row, 1)
        
    def set_widgets(self):
        self.setWindowTitle('PET Frame Times')
        
class FrameTimeModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data
        
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.iloc[index.row()][index.column()]))
        return QtCore.QVariant()

class FrameTimeController(ControllerBase):
    def __init__(self, view=None, model=None):
        if view is None:
            view = FrameTimeWidget()
        super().__init__(view=view, model=model)
        self.view.table.setModel(self.model)
        
    def set_view_callbacks(self):
        self.view.close_button.clicked.connect(self.close)
        self.view.export_button.clicked.connect(self.export)
    
    def close(self):
        self.view.close()
    
    def export(self):
        filename, _ = QFileDialog.getSaveFileName(parent=self.view,
                                                  caption='Export to Excel',
                                                  filter="Excel (*.xlsx)")
        
        if filename:
            self.model._data.to_excel(filename)

class IconLabel(QWidget):

    IconSize = QtCore.QSize(16, 16)
    HorizontalSpacing = 2
    
    _icon_ok = None
    _icon_missing = None

    def __init__(self, text='', ok=True, final_stretch=True):
        super(QWidget, self).__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.icon = QLabel()
        #self.icon.setPixmap(qta.icon(self.get_icon_ok().pixmap(self.IconSize))
        
        layout.addWidget(self.icon)
        layout.addSpacing(self.HorizontalSpacing)
        layout.addWidget(QLabel(text))

        if final_stretch:
            layout.addStretch()
        self.set_ok(ok)
        
    def get_icon_ok(self):
        if self._icon_ok is None:
            self._icon_ok = qta.icon("ei.ok-sign",color='green')
        return self._icon_ok
    
    def get_icon_missing(self):
        if self._icon_missing is None:
            self._icon_missing = qta.icon("ei.remove-sign",color='red')
        return self._icon_missing
        
        
    def set_ok(self, ok):
        
        if ok:    
            self.icon.setPixmap(self.get_icon_ok().pixmap(self.IconSize))
            self.icon.setToolTip('Value was found in dicom header')
        else:
            self.icon.setPixmap(self.get_icon_missing().pixmap(self.IconSize))
            self.icon.setToolTip('Value was not found in dicom header')


class SUVWidget(WidgetBase):
    WEIGHT = 'weight'
    ACTIVITY = 'activity'
    HALFLIFE = 'halflife'
    
    SCANDATE = 'scandate'
    SCANTIME = 'scantime'
    
    ACTIVITYDATE = 'activitydate'
    ACTIVITYTIME = 'activitytime'
    
    ITEMS = [WEIGHT, SCANTIME, SCANDATE, ACTIVITY, ACTIVITYTIME, ACTIVITYDATE,
             HALFLIFE]
    
    
    
    def create_widgets(self):
        self.labels = {}
        self.widgets = {}
        
        self.title_label                  = QLabel('Edit SUV Parameters')        
        self.labels[self.WEIGHT]          = IconLabel('Patient Weight [kg]')
        self.widgets[self.WEIGHT]         = QDoubleSpinBox()
        self.labels[self.SCANTIME]        = IconLabel('Start Scan Time [hh:mm:ss]')
        self.widgets[self.SCANTIME]       = QTimeEdit()  
        self.labels[self.SCANDATE]        = IconLabel('Start Scan Date [dd-mm-yyyy]')
        self.widgets[self.SCANDATE]       = QDateEdit()
        self.labels[self.ACTIVITY]        = IconLabel('Injected Activity [MBq]')
        self.widgets[self.ACTIVITY]       = QDoubleSpinBox()
        self.labels[self.ACTIVITYTIME]    = IconLabel('Activity Time')
        self.widgets[self.ACTIVITYTIME]   = QTimeEdit()
        self.labels[self.ACTIVITYDATE]    = IconLabel('Activity Date')
        self.widgets[self.ACTIVITYDATE]   = QDateEdit()
        self.labels[self.HALFLIFE]        = IconLabel('Halflife [min]')
        self.widgets[self.HALFLIFE]       = QDoubleSpinBox()
        
        
    def set_widgets(self):
        self.widgets[self.WEIGHT].setMaximum(500)
        self.widgets[self.SCANTIME].setDisplayFormat("HH:mm:ss")
        self.widgets[self.ACTIVITY].setMaximum(10E3)
        self.widgets[self.ACTIVITYTIME].setDisplayFormat("HH:mm:ss")
        self.widgets[self.HALFLIFE].setMaximum(50E6)
        self.widgets[self.SCANDATE].setDisplayFormat('dd-MM-yyyy')        
        self.widgets[self.ACTIVITYDATE].setDisplayFormat('dd-MM-yyyy')
        
    def create_layout(self):
        row = 0
        
        self.layout.addWidget(self.title_label, row, 0, 1, 2)

        for row, key in enumerate(self.ITEMS):
            self.layout.addWidget(self.labels[key], row + 1, 0)
            self.layout.addWidget(self.widgets[key], row + 1, 1)

    def from_dict(self, value_dict):
        def set_widget_and_label(widget, label, value):
            ok = value is not None            
            label.set_ok(ok)
            set_widget(widget, value)
        
        for key in self.ITEMS:
            set_widget_and_label(self.widgets[key], 
                                 self.labels[key], 
                                 value_dict[key])
                
    def to_dict(self):
        value_dict = {}
        for key in self.ITEMS:
            value_dict[key] = get_widget(self.widgets[key])
        return value_dict
    
    def from_dicom_dict(self, dicom_dict):
        value_dict = {}
        value_dict[self.WEIGHT] = dicom_dict['PatientWeight']
        value_dict[self.ACTIVITY] = dicom_dict['RadionuclideTotalDose'] / 1E6
        value_dict[self.ACTIVITYDATE] = dicom_dict['SeriesDateTime'].date()
        value_dict[self.ACTIVITYTIME] = dicom_dict['SeriesDateTime'].time()
        value_dict[self.SCANTIME] = dicom_dict['RadiopharmaceuticalStartDateTime'].time()
        value_dict[self.SCANDATE] = dicom_dict['RadiopharmaceuticalStartDateTime'].date()
        value_dict[self.HALFLIFE] = dicom_dict['RadionuclideHalfLife'] / 60

        self.from_dict(value_dict)
    
    def to_dicom_dict(self):
        value_dict = self.to_dict()
        dicom_dict = {}
       
        scan_dt = datetime.combine(value_dict[SUVWidget.SCANDATE], 
                                   value_dict[SUVWidget.SCANTIME])
        
        activity_dt = datetime.combine(value_dict[SUVWidget.ACTIVITYDATE], 
                                       value_dict[SUVWidget.ACTIVITYTIME])
        
        dicom_dict['RadiopharmaceuticalStartDateTime'] = activity_dt
        dicom_dict['SeriesDateTime'] = scan_dt
        
        dicom_dict['PatientWeight'] = value_dict[SUVWidget.WEIGHT]
        dicom_dict['RadionulcideTotalDose'] = value_dict[SUVWidget.ACTIVITY] * 1E6
        return dicom_dict
    
class LoadOptionsWidget(WidgetBase):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.dynamic_check.clicked.connect(self.update_dynamic_check)

        self.update_dynamic_check()

        
    def update_dynamic_check(self):        
        enabled = self.dynamic_check.isChecked()
        self.tag_label.setEnabled(enabled)
        self.tag_input.setEnabled(enabled)
        self.duration_label.setEnabled(enabled)
        self.duration_input.setEnabled(enabled)
        
   
    
    def create_widgets(self):
        self.bqml_radio  = QRadioButton('Units Bq/ml or counts')
        self.suv_radio = QRadioButton('Units SUV')
        
        
        self.suv_radio.setChecked(True)
        
        self.dynamic_check = QCheckBox('Load dynamic PET Data')
        self.tag_label = QLabel('Use tag to identify mid frame time: ')
        self.tag_input = QLabel('FrameReferenceTime')
        self.duration_label = QLabel('Use tag to identify frame duration: ')
        self.duration_input = QLabel('ActualFrameDuration')
        
    def create_layout(self):
        row = 0
        
        self.layout.addWidget(self.bqml_radio, row, 0)
        self.layout.addWidget(self.suv_radio, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.dynamic_check, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.tag_label, row, 0)
        self.layout.addWidget(self.tag_input, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.duration_label, row, 0)
        self.layout.addWidget(self.duration_input, row, 1)
        

class LoadPETDialog(QDialogBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_options_widget.suv_radio.toggled.connect(self.update_suv_check)
        self.load_options_widget.bqml_radio.toggled.connect(self.update_suv_check)
        self.update_suv_check()
        
    def create_widgets(self):
        self.folder_button = QPushButton('Select Folder')
        self.folder_label = QLabel('Select Folder')
        self.suv_widget = SUVWidget()
        
        self.load_options_widget = LoadOptionsWidget()
        
        self.loadpet_button = QPushButton('Load PET')
        self.cancel_button = QPushButton('Cancel')
        self.frametime_button = QPushButton('See Frame Times')
        
        self.setWindowTitle('Load PET from DICOM')
        self.update_suv_check()
    
    def update_suv_check(self):
        enabled = self.load_options_widget.suv_radio.isChecked()
        self.suv_widget.setEnabled(enabled)
        
    def create_layout(self):
        row = 0
        self.layout.addWidget(self.suv_widget, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.load_options_widget, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.folder_label, row, 0)
        row += 1
        
        self.layout.addWidget(self.folder_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.frametime_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.loadpet_button, row, 0)
        self.layout.addWidget(self.cancel_button, row, 1)
        

        
class LoadPETController(ControllerBase):
    folder = 'test'
    image = None
    def __init__(self, parent=None, view=None):
        if view is None:
            view = LoadPETDialog(parent=parent)
        super().__init__(view=view)
        self.update_enabled()
      
    def set_view_callbacks(self):

        self.view.folder_button.clicked.connect(self.select_folder)
        self.view.loadpet_button.clicked.connect(self.load_pet)
        self.view.cancel_button.clicked.connect(self.cancel)
        self.view.frametime_button.clicked.connect(self.show_frame_times)
        
    def show_frame_times(self):
        model = FrameTimeModel(self.read_frame_times())
        view = FrameTimeWidget(parent=self.view)
        contr = FrameTimeController(model=model, view=view)
        contr.view.show()
        contr.view.exec_()
            
        
    def cancel(self):
        self.image = None
        self.view.close()
    
    def load_pet(self):
        if not self.folder_is_valid():
            return
        
        dynamic = self.view.load_options_widget.dynamic_check.isChecked()
        frame_tagname = self.view.load_options_widget.tag_input.text()
        suv = self.view.load_options_widget.suv_radio.isChecked()
        
        if not dynamic:

            image = sitk_tools.read_folder(self.folder, 
                                          SUV=suv, 
                                          recursive=True)
            self.image = image
        else:
  
            image_dict = sitk_tools.read_frames_from_folder(self.folder, 
                                               SUV=False, 
                                               frame_tag=frame_tagname, 
                                               recursive=True)
            frames = [image_dict[key] for key in sorted(list(image_dict.keys()))]
            self.image = sitk.JoinSeries(frames)
        self.view.close()
        return
        
        
    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(None, 'Select a folder:', 
                                                  '~', 
                                                  QFileDialog.ShowDirsOnly)

        if folder:
            self.folder = folder
        self.update()

        
    def folder_is_valid(self):
        return self.folder is not None and os.path.exists(self.folder)

    def update_enabled(self):
        enabled = self.folder_is_valid()
        self.view.suv_widget.setEnabled(enabled)
        self.view.load_options_widget.setEnabled(enabled)
        self.view.loadpet_button.setEnabled(enabled)
        if enabled:
            self.view.load_options_widget.update_dynamic_check()
            
    def read_frame_times(self):
        if self.folder is None:
            return
        series_reader = sitk.ImageSeriesReader()
        files  = series_reader.GetGDCMSeriesFileNames(self.folder, 
                                                      recursive=True)
        
        reader = sitk.ImageFileReader()
        dicom_dict = {'FrameReferenceTime': '0054|1300', 
                      'ActualFrameDuration': '0018|1242'}
                      
        
        values = {key: [] for key in dicom_dict.keys()}
        for file in files:
            reader.SetFileName(file)
            reader.ReadImageInformation()
            for name, tag in dicom_dict.items():
                values[name].append(reader.GetMetaData(tag))
        
        frame_times = values['FrameReferenceTime']
        unique_frame_times = list(set(frame_times))
        
        frame_duration = values['ActualFrameDuration']
        unique_frame_duration = [frame_duration[frame_times.index(ftime)]\
                                 for ftime in unique_frame_times]
            
        
        frame_times = [(float(ftime)/1000) for ftime in unique_frame_times]
        frame_duration = [(float(fdur)/1000) for fdur in unique_frame_duration]
        
        sort_order = np.argsort(frame_times)
    
        frame_times = [frame_times[i] for i in sort_order]
        frame_duration = [frame_duration[i] for i in sort_order]
        
        frame_start = [ftime - 0.5 * fdur\
                       for ftime, fdur in zip(frame_times, frame_duration)]
            
        frame_end = [ftime + 0.5 * fdur\
                     for ftime, fdur in zip(frame_times, frame_duration)]
            
        data = pd.DataFrame()
        data['frame start [s]'] = frame_start
        data['frame end [s]'] = frame_end
        data['frame center [s]'] = frame_times
        data['frame_duration [s]'] = frame_duration
        
        for col in data.columns:
            data[col] = data[col].round(1)
            
        return data
        
            
        
        
                        
    def update(self):
        if not self.folder_is_valid():
            self.update_enabled()
            return
        
      
        reader = sitk.ImageSeriesReader()
        files  = reader.GetGDCMSeriesFileNames(self.folder, recursive=True)
        reader.SetMetaDataDictionaryArrayUpdate(True)
        
        
        
        if len(files) == 0:
            self.folder = f'No Dicom files found in: {self.folder}'                
        else:

            header = pydicom.read_file(files[0], stop_before_pixels=True)
            suv_params = sitk_tools.suv_parameters_from_header(header)
            self.view.suv_widget.from_dicom_dict(suv_params)
        
        
        if self.folder is not None:
            self.view.folder_label.setText(self.folder)
        self.update_enabled()
        
if __name__ == "__main__":
   
    
    app = QApplication([])
    view = LoadPETDialog()
    #view.suv_widget.from_dicom_dict(dicom_dict)
    contr = LoadPETController(view=view)
    contr.folder = 'D:/PUMP/Arterieel/PET_PUMP2_LEVER_DYN_AC'
    view.show()
    app.exec_()
    
    view.suv_widget.to_dict()
        

