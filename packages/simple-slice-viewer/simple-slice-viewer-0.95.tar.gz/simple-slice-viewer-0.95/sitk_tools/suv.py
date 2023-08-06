import sitk_tools as sitktools
import SimpleITK as sitk
import dateutil

def get_suv_attr(header, attr):        
    if attr == 'SeriesDateTime':
        # return SeriesDateTime if availble otherwise SeriesDate + SeriesTime
        if hasattr(header, attr):
            return getattr(header, attr)
        elif hasattr(header, 'SeriesDate') and hasattr(header, 'SeriesTime'):
            return header.SeriesDate + header.SeriesTime
        
    if attr == 'RadiopharmaceuticalStartDateTime':
        # return StartDateTime if available otherwises SeriesDate + StartTime
        nuclideinfo = get_suv_attr(header, 
                                   'RadiopharmaceuticalInformationSequence')[0]
        
        if hasattr(nuclideinfo, attr) and getattr(nuclideinfo, attr) not in (None, ''):
            return getattr(nuclideinfo, attr)
        elif hasattr(nuclideinfo, 'RadiopharmaceuticalStartTime') and hasattr(header, 'SeriesDate'):
            halflife = float(get_suv_attr(nuclideinfo, 'RadionuclideHalfLife'))
            if halflife > (3600 * 7):
                # for long lived isotopes SeriesDate cannot be reliably used
                raise ValueError('SeriesDate cannot be used as calibration date for long lived isotopes!')
            return header.SeriesDate + nuclideinfo.RadiopharmaceuticalStartTime

    if not hasattr(header, attr):
        raise AttributeError(f'Missing for SUV calculation: {attr}')
    return getattr(header, attr)
    
def parse_datetime(date_time_string):
    try:
        dt = dateutil.parser.parse(date_time_string.split('.')[0])
    except:
        raise ValueError(f'Could cot parse date time string: {date_time_string}')
    return dt

def suv_scale_factor(header):
    suv_params = suv_parameters_from_header(header)
    
    series_dt           = suv_params['SeriesDateTime']
    injection_dt        = suv_params['RadiopharmaceuticalStartDateTime']
    halflife            = suv_params['RadionuclideHalfLife']
    nuclide_dose        = suv_params['RadionuclideTotalDose']
    patient_weight      = suv_params['PatientWeight']
    delta_time          = (series_dt - injection_dt).total_seconds()
    decay_correction    = 0.5 ** (delta_time / halflife)
    suv_scaling         = (patient_weight * 1000) / (decay_correction * nuclide_dose)
    
    return suv_scaling
    
    

def suv_parameters_from_header(header, allow_missing_tags=False):
   
    try:
        nuclide_info   = get_suv_attr(header, 
                                      'RadiopharmaceuticalInformationSequence')[0]
    except:
        if allow_missing_tags:
            nuclide_info = None
        else:
            raise
            
            
    try:
        series_dt = parse_datetime(get_suv_attr(header, 'SeriesDateTime'))
    except:
        if allow_missing_tags:
            series_dt = None
        else:
            raise
    
    try:
        injection_dt = parse_datetime(get_suv_attr(header, 'RadiopharmaceuticalStartDateTime'))
    except:
        if allow_missing_tags:
            injection_dt = None
        else:
            raise
        
    try:
        nuclide_dose   = float(get_suv_attr(nuclide_info,  'RadionuclideTotalDose'))
    except:
        if allow_missing_tags:
            nuclide_dose = None
        else:
            raise
            
    try:
        patient_weight = float(get_suv_attr(header,        'PatientWeight'))
    except:
        if allow_missing_tags:
            patient_weight = None
        else:
            raise
            
    try:
        halflife      = float(get_suv_attr(nuclide_info,   'RadionuclideHalfLife'))
    except:
        if allow_missing_tags:
            halflife = None
        else:
            raise
    
    suv_params = {'RadiopharmaceuticalStartDateTime':      injection_dt,
                  'SeriesDateTime':                        series_dt,
                  'PatientWeight':                         patient_weight,
                  'RadionuclideHalfLife':                  halflife,
                  'RadionuclideTotalDose':                 nuclide_dose}


    return suv_params







def _minimal_mask(image, mask):
    
    max_value = sitktools.max(image, mask)
    max_location = sitktools.find_phys(image, value=max_value)[0]
    minimal_mask = sitktools.sphere(image, center=max_location,
                                    radius=6)
    
    if sitktools.isempty(mask): # very large voxels?
        minimal_mask = sitktools.zeros_like_image(image)
        # make at least one voxel 1
        minimal_mask[mask.TransformPhysicalPointToIndex(max_location)] = 1
    return minimal_mask

def SUVpeak(image, mask=None, peak_voi_radius=6):
    """
    Calculate SUVpeak for image. Specify a mask to find SUVpeak in a smaller
    region. If no mask and specified and image is large computation takes
    some time.

    Parameters
    ----------
    image : sitk.Image
        SimpleITK image. Image for which SUVpeak is calculated
    mask : sitk.Image
        SimpleITK mask (sikt.sitkUINT8). If specified determine SUVpeak for
        this region.
    peak_voi_radius : float, optional
        SUVpeak region has a radius of 6mm by default (sphere volume appr 1ml).


    Returns
    -------
    float
        SUVpeak.

    """
    if mask:
        # reduce computational load
        image = sitktools.crop_by_mask(image, mask, margin=peak_voi_radius)
        mask = sitktools.crop_by_mask(mask, mask, margin=peak_voi_radius)
        
        if sitktools.isempty(mask):
            mask = _minimal_mask(image, mask)

    center = sitktools.center_phys(image)

    kernel = sitktools.shapes.sphere(image=image,
                                     center=center,
                                     radius=peak_voi_radius)

    # note spacing and origin of kernel are ignored. Pixel ID must match
    # image pixel ID
    kernel = sitktools.crop_by_mask(kernel, kernel, margin=peak_voi_radius)

    kernel = sitk.Cast(kernel, image.GetPixelID())

    # normalize kernel in process
    SUVpeak_image = sitk.Convolution(image, kernel, normalize=True)

    return sitktools.max(SUVpeak_image, mask=mask)
