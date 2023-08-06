# README #

## Overview

A viewer to scroll through slices of 2D, 3D and 4D medical data sets 
(CT, PET, MRI...)

Supports files than can be read by SimpleITK:

* Nifti: .nii .nii.gz .nia .img .img.gz .hdr
* Nrrd:  .nrrd .nhdr
* Meta Image: .mhd .mha 

And probably some more types as long as they are supported by the SimpleITK
file reader.

In addition there is support for reading folders with dicom data. 
Sorting dicom data into 3D volume is tricky and may depend on modality, vendor
and model of the imaging device. Basic support is offered that works well with
CT, PET and MRI. For Siemens PET the PET data is read in SUV.

A second image can be loaded and is displayed as fusion on top of the first.
Works well with PET/CT and PET/MRI data.



##Usage

pip install simple-slice-viewer

### Command Line
    simple-slice-viewer
    simple-slice-viewer ct.nii
    simple-slice-viewer ct.nii --fusion pet.nii
    

or use ssv as shorthand:
    ssv
    ssv ct.nii
    ssv ct.nii --fusion pet.nii
    ssv --image ct.nii --fusion pet.nii

### Inside Python

In Python images should be read to SimpleITK Image objects first.

    import simple_slice_viewer as ssv
    import SimpleITK as sikt

    image = sitk.ReadImage('ct.nii')
    fusion = sitk.ReadImage('pet.nii')

    ssv.display(image=image, fusion=fusion)
    

To display a numpy array convert it to SimpleITK first

    import SimpleITK as sitk
    import simple_slice_viewer as ssv
    image = sitk.GetImageFromArray(np_array)
    ssv.display(image)



