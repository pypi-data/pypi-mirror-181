import cv2
import qimage2ndarray
from PyQt5.QtWidgets import QLabel, QFileDialog, QSpinBox, QPushButton, QCheckBox, QProgressBar
from simple_slice_viewer.controller_base import ControllerBase
from simple_slice_viewer.preset_view import QDialogBase

DEFAULT_FPS = 10

class MovieMakerView(QDialogBase):
    def create_widgets(self):
        self.setWindowTitle('Export Movie')
        self.start_label = QLabel('Start index: ')
        self.start_value = QSpinBox()
        self.end_label = QLabel('End index: ')
        self.end_value = QSpinBox()
        self.colorbar_check = QCheckBox('Show Colorbar')
        self.colorbarfusion_check = QCheckBox('Show Fusion Colorbar')
        self.file_label = QLabel('Select File...')
        self.file_button = QPushButton('Export Movie')
        self.fps_label = QLabel('Frames per second: ')
        self.fps_value = QSpinBox()
        self.fps_value.setMaximum(60)
        self.fps_value.setMinimum(1)
        self.fps_value.setValue(DEFAULT_FPS)
        self.progressbar = QProgressBar()
        
        
    def create_layout(self):
        row = 0
        
        self.layout.addWidget(self.start_label, row, 0)
        self.layout.addWidget(self.start_value, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.end_label, row, 0)
        self.layout.addWidget(self.end_value, row, 1)
        
        row += 1
        self.layout.addWidget(self.colorbar_check, row , 0)
        self.layout.addWidget(self.colorbarfusion_check, row , 1)
        
        row += 1
        
        self.layout.addWidget(self.fps_label, row, 0)
        self.layout.addWidget(self.fps_value, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.file_label, row, 0, 1, 2)
        
        
        row += 1
        
        self.layout.addWidget(self.file_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.progressbar, row, 0, 1, 2)
        self.progressbar.setVisible(False)
        
         
class MovieMaker(ControllerBase):
    FRAMES = 'frames'
    SLICES = 'slices'
    filename = None
    def __init__(self, view=None, model=None, image_view=None,
                 movie_type='slices'):
        
        
        self.model = model
        self.image_view = image_view
        self.movie_type = movie_type
        if view is None:
            view = MovieMakerView(parent=self.image_view)
        self.view = view
        
        self.set_view()
        
    def get_file_to_write(self):
        extension = "MP4 (*.mp4)"
        filename = QFileDialog.getSaveFileName(self.view, 'Select a file:', 
                                           'movie.mp4',
                                            filter=extension)
        filename = filename[0]
        if not filename:
            return

        self.view.file_label.setText(filename)
        show_colorbar = self.view.colorbar_check.isChecked()
        show_colorbarfusion = self.view.colorbarfusion_check.isChecked()
        start = self.view.start_value.value()
        end = self.view.end_value.value()
        fps = self.view.fps_value.value()
        if self.movie_type == self.SLICES:
            self.write_movie_slices(filename, fps=fps, start=start, end=end,
                                    show_image_colorbar=show_colorbar,
                                    show_fusion_colorbar=show_colorbarfusion)
        elif self.movie_type == self.FRAMES:
            self.write_movie_frames(filename, fps=fps, start=start, end=end,
                                    show_fusion_colorbar=show_colorbarfusion,
                                    show_image_colorbar=show_colorbar)
        
            
        
    def set_view(self):
        
        if self.movie_type == self.SLICES:
            movie_frames = self.model.get_number_of_slices()            
        else:
            movie_frames = self.model.get_number_of_frames()
        
        self.view.end_value.setMaximum(movie_frames)
        self.view.end_value.setValue(movie_frames)
        
        
        enabled = self.image_view.colorbar_image.isVisible()
            
        self.view.colorbar_check.setEnabled(enabled)
        self.view.colorbar_check.setChecked(enabled)
        
        enabled = self.image_view.colorbar_fusion.isVisible()
        self.view.colorbarfusion_check.setEnabled(enabled)
        self.view.colorbarfusion_check.setChecked(enabled)

        self.view.file_button.clicked.connect(self.get_file_to_write)
        
    
    def write_movie_slices(self, filename='movie.mp4', fps=1, start=0, 
                           end=100, show_image_colorbar=False, 
                           show_fusion_colorbar=False):
        
        current_index = self.model.get_index()        
        
        self._write_movie(filename=filename, fps=fps, start=start, end=end,
                          frame_setter=self.model.set_index, 
                          show_image_colorbar=show_image_colorbar, 
                          show_fusion_colorbar=show_fusion_colorbar)
        
        self.model.set_index(current_index)
        
    def write_movie_frames(self, filename='movie.mp4', fps=1, start=0, 
                           end=100, show_image_colorbar=False, 
                           show_fusion_colorbar=False):
        
        current_index = self.model.get_frame_index()        
        
        self._write_movie(filename=filename, fps=fps, start=start, end=end,
                          frame_setter=self.model.set_frame_index, 
                          show_image_colorbar=show_image_colorbar, 
                          show_fusion_colorbar=show_fusion_colorbar)
        
        self.model.set_frame_index(current_index)
        
        
    def _write_movie(self, filename='movie.mp4', fps=1, start=0,
                     end=100, frame_setter=None, show_image_colorbar=False,
                     show_fusion_colorbar=False):
        if fps == 1:
            raise
        
        
        if not show_image_colorbar:
            cbar = self.image_view.colorbar_image
            cbar_image_visible = cbar.isVisible()
            cbar.setVisible(False)

        if not show_fusion_colorbar:
            cbar = self.image_view.colorbar_fusion
            cbar_fusion_visible = cbar.isVisible()
            cbar.setVisible(False)

            
        video_writer = self.get_video_writer(filename=filename, fps=fps)
        
        self.view.progressbar.setMaximum(end)
        self.view.progressbar.setMinimum(start)
        self.view.progressbar.setVisible(True)
        for index in range(start, end):       
            self.view.progressbar.setValue(index)
            frame_setter(index)
            video_writer.write(cv2.cvtColor(self.get_nparray(), cv2.COLOR_RGB2BGR))                                
        video_writer.release()
        
        if not show_image_colorbar:
            self.image_view.colorbar_image.setVisible(cbar_image_visible)
            
        if not show_fusion_colorbar:
            self.image_view.colorbar_fusion.setVisible(cbar_fusion_visible)
            
        self.view.progressbar.setVisible(False)
        
        
    def get_video_writer(self, filename='movie.mp4', fps=1):
        # FourCC is a 4-byte code used to specify the video codec.
        fourcc = cv2.VideoWriter_fourcc(*"mp4v") 
        dummy_array = self.get_nparray()
        shape = dummy_array.shape[0:2]

        writer = cv2.VideoWriter(filename, fourcc, float(fps), (shape[1], shape[0]))
        return writer
        
    def get_qtimage(self):
        return self.image_view.glayout.grab().toImage()
    
    def get_nparray(self):
        return qimage2ndarray.rgb_view(self.get_qtimage())
    
if __name__ == "__main__":
    app = QApplication([])
    view = MovieMakerView()
    view.show()
    view.exec_()