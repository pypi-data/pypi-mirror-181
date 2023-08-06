import SimpleITK as sitk
import pydicom
import os
import numpy as np
import sitk_tools

SUV_SCALE_FACTOR = 'SUVScaleFactor'

class HermesSegmentation:
    _dcm = None
    _labeled_mask = None
    _mask = None
    
    MASK_LABEL = 'hermes_mask'
    BACKGROUND_LABEL = 'TumorFinder:Background'
    
    def __init__(self, folder=None):
        self.folder = folder
        
    @property
    def files(self):
        return [os.path.join(self.folder, fi) for fi in os.listdir(self.folder)]
        
    def get_image(self, label=None):
        pass
    
    def _is_bkg_dcm(self, dcm):
        return dcm.SegmentSequence[0].SegmentDescription == self.BACKGROUND_LABEL
    
    def _get_label(self, dcm):
        return dcm.SegmentSequence[0].SegmentDescription
    
    def _get_index(self, dcm):
        return int(self._get_label(dcm).split(' ')[-1])
    
    def save(self, folder):
        sitk.WriteImage(self.labeled_mask, os.path.join(folder, self.MASK_LABEL + '.nii'))
    
    @property
    def dcm(self):
        if self._dcm is None:
            dcm = [pydicom.read_file(file) for file in self.files]
            dcm = [dcmi for dcmi in dcm if not self._is_bkg_dcm(dcmi)]
            
            indices = [self._get_index(dcmi) for dcmi in dcm]
            dcm = [dcm[index] for index in np.argsort(indices)]
            self._dcm = dcm
        return self._dcm
    
    @property
    def labeled_mask(self):
        if self._labeled_mask is None:
            masks = []
            for index, dcmi in zip(self.indices, self.dcm):
                mask_index = read_seg(dcmi) * index
                masks += [mask_index]
            self._labeled_maks = sum(masks)
        return self._labeled_maks

    @property
    def mask(self):
        return self._labeled_mask > 0        
    
    def get_mask(self, index=None):
        if index is None:
            mask = self.mask
        else:
            mask = self.labeled_mask == index
        return mask
    
    def get_mask_volume(self, index=None):
        mask = self.get_mask(index=index)
        return sitk_tools.voxel_volume_ml(mask) * sitk_tools.sum(mask)
    
    def get_tumor_tlg(self, image, index=None):
        mask = self.get_mask(index=index)
        return sitk_tools.sum(image, mask=mask)
            
    @property
    def indices(self):         
        return [self._get_index(dcmi) for dcmi in self.dcm]
        
    
    @property
    def labels(self):
        return [self._get_label(dcmi) for dcmi in self.dcm]
        
        


def sort_files_by_slice_position(files):
    
    reader = sitk.ImageFileReader()
    
    origins = []
    for file in files:    
        reader.SetFileName(file)
        reader.ReadImageInformation()
        origins += [reader.GetOrigin()]
        
    direction = reader.GetDirection()
    
    
    slice_dir = np.asarray(direction[-3:])
    
    distances =  []
    for index, origin in enumerate(origins):
        distance_slice_dir = sum([i*j for i, j in zip(slice_dir, origin)])
        distances += [distance_slice_dir]
    
    order = [i for (v, i) in sorted((v, i) for (i, v) in enumerate(distances))]
    files = [files[i] for i in order]
    return files, order
    


def get_series_instance_uids(files):
    folders = set()
    for file in files:
        folders.add(os.path.split(file)[0])

    reader = sitk.ImageSeriesReader()

    ids = []
    reader.SetGlobalWarningDisplay(False)
    for folder in folders:
        if folder == '':
            folder = '.'
        ids += list(reader.GetGDCMSeriesIDs(folder))

    reader.SetGlobalWarningDisplay(True)

    return ids

def get_tag_from_file(file, tag, reader=None):
    tag = tagname_to_sitk_tag(tag)
    
    if reader is None:
        reader = sitk.ImageFileReader()
    
    if isinstance(file, (list, tuple)):
        return [get_tag_from_file(fi, tag, reader=reader) for fi in file]
    
    reader.SetFileName(file)
    reader.ReadImageInformation()
    value = reader.GetMetaData(tag)
    
    try:
        value = float(value)
    except ValueError:
        pass
    
    return value

def tagname_to_sitk_tag(tagname):
    if len(tagname) == 9 and tagname[4] == '|':
        return tagname
    
    tagnumber=pydicom.datadict.tag_for_keyword(tagname)
    tag = pydicom.tag.Tag(tagnumber)
    
    group = str(hex(tag.group)).split('0x')[1]
    element = str(hex(tag.element)).split('0x')[1]
    
    group = group.rjust(4, '0')
    element = element.rjust(4, '0')
    
    sitk_tag = group + '|' + element
    return sitk_tag

def validate_series_instance_uid(files):
    series_instance_uids = get_series_instance_uids(files)
    
    if len(series_instance_uids) == 0:
        raise IOError('No dicom files found!')
    elif len(series_instance_uids) > 1:
        raise IOError('Multiple Dicom Series Found!')
        

def read_folder(folder, SUV=False, frame_tag=None, recursive=False):
    reader = sitk.ImageSeriesReader()
    files  = reader.GetGDCMSeriesFileNames(folder, recursive=recursive)
    return read_files(files, SUV=SUV)


def read_frames_from_folder(folder, SUV=False, frame_tagname=None, recursive=False):
    reader = sitk.ImageSeriesReader()
    files  = reader.GetGDCMSeriesFileNames(folder, recursive=recursive)
    return read_frames_from_files(files, SUV=SUV, frame_tagname=frame_tagname)
        
def read_frames_from_files(files, SUV=None, frame_tagname=None):
    if frame_tagname is None:
        return read_files(files, SUV=SUV)
    
    sitk_tag = tagname_to_sitk_tag(frame_tagname)
    tag_values = get_tag_from_file(files, sitk_tag)
    
    split = {}
    for file, tag_value in zip(files, tag_values):
        if tag_value not in split.keys():
            split[tag_value] = []
        split[tag_value] += [file]
        
    frames = {}
    for tag_value, fns in split.items():
        frames[tag_value] = read_files(fns, SUV=SUV)

    return frames


def read_files(files, SUV=False):
    validate_series_instance_uid(files)
    
    reader = sitk.ImageSeriesReader()

    files, _ = sort_files_by_slice_position(files)
    
    reader.SetFileNames(files)
    image = reader.Execute()
    
    modality = get_tag_from_file(files[0], '0008|0060')
    if SUV and modality in ('PT', 'NM'):
       header = pydicom.read_file(files[0], stop_before_pixels=True)       
       suv_factor = sitk_tools.suv.suv_scale_factor(header)
       image *= suv_factor

    return image



def read_file(file, SUV=False):
    reader = sitk.ImageFileReader()
    reader.SetFileName(file)
    image = reader.Execute()

    modality = get_tag_from_file(file, '0008|0060')
    if SUV and modality in ('PT', 'NM'):
       header = pydicom.read_file(file, stop_before_pixels=True)       
       suv_factor = sitk_tools.suv.suv_scale_factor(header)
       image *= suv_factor
    

    return image
    

def read_seg(file_data):
    if isinstance(file_data, str) and os.path.isdir(file_data):
        file_data = [os.path.join(file_data, file)\
                     for file in os.listdir(file_data)]
        return read_seg(file_data)
    elif isinstance(file_data, (list, tuple)):
        return sum([read_seg(file) for file in file_data])
    
    elif isinstance(file_data, str):
        return read_seg(pydicom.read_file(file_data))

    dcm = file_data
    
    direction = dcm.SharedFunctionalGroupsSequence[0].PlaneOrientationSequence[0].ImageOrientationPatient
    direction = dcm_to_sitk_orientation(direction)
    origin, extent = get_image_origin_and_extent(dcm, direction)
    
    
    
    
    spacing = dcm.SharedFunctionalGroupsSequence[0].PixelMeasuresSequence[0].PixelSpacing
    slice_thickness = dcm.SharedFunctionalGroupsSequence[0].PixelMeasuresSequence[0].SliceThickness

    image = sitk.GetImageFromArray(dcm.pixel_array)
    

    image.SetOrigin(origin)
    image.SetSpacing([float(spacing[0]), float(spacing[1]), float(slice_thickness)])
    image.SetDirection(direction.ravel())
    
    return image
    
def dcm_to_sitk_orientation(iop):

    assert len(iop) == 6


    # Extract x-vector and y-vector

    x_dir = [float(x) for x in iop[:3]]

    y_dir = [float(x) for x in iop[3:]]


    # L2 normalize x-vector and y-vector

    x_dir /= np.linalg.norm(x_dir)

    y_dir /= np.linalg.norm(y_dir)


    # Compute perpendicular z-vector

    z_dir = np.cross(x_dir, y_dir)


    return np.stack([x_dir, y_dir, z_dir], axis=1)




def get_image_origin_and_extent(dataset, direction):

    frames = dataset.PerFrameFunctionalGroupsSequence

    slice_dir = direction[:, 2]

    reference_position = np.asarray([float(x) for x in frames[0].PlanePositionSequence[0].ImagePositionPatient])


    min_distance = 0.0

    origin = (0.0, 0.0, 0.0)

    distances = {}

    for frame_idx, frame in enumerate(frames):

        frame_position = tuple(float(x) for x in frame.PlanePositionSequence[0].ImagePositionPatient)

        if frame_position in distances:

            continue


        frame_distance = np.dot(frame_position - reference_position, slice_dir)

        distances[frame_position] = frame_distance


        if frame_idx == 0 or frame_distance < min_distance:

            min_distance = frame_distance

            origin = frame_position


    # Sort all distances ascending and compute extent from minimum and

    # maximum distance to reference plane

    distance_values = sorted(distances.values())

    extent = 0.0

    if len(distance_values) > 1:

        extent = abs(distance_values[0] - distance_values[-1])


    return origin, extent



    


