import os
from aicsimageio import AICSImage
from tifffile import imsave
from pathlib import Path
import numpy as np
from skimage.filters import threshold_otsu
from skimage.morphology import ball, binary_closing, remove_small_objects, dilation, erosion, disk
from aicssegmentation.core.pre_processing_utils import  intensity_normalization, edge_preserving_smoothing_3d
from aicssegmentation.core.vessel import vesselness3D
from aicssegmentation.core.seg_dot import dot_2d
from aicssegmentation.core.utils import topology_preserving_thinning, hole_filling
import matplotlib.pyplot as plt
from itkwidgets import view   
from aicssegmentation.core.visual import seg_fluo_side_by_side,  single_fluorescent_view, segmentation_quick_view
plt.rcParams["figure.figsize"] = [16, 12]
from aicssegmentation.core.MO_threshold import MO
from aicspylibczi import CziFile

# dots|
from aicssegmentation.core.seg_dot import dot_3d, dot_3d_wrapper 
from aicssegmentation.core.seg_dot import dot_2d_slice_by_slice_wrapper
from aicssegmentation.core.pre_processing_utils import intensity_normalization, image_smoothing_gaussian_slice_by_slice
from skimage.morphology import remove_small_objects, dilation, erosion, ball     # function for post-processing (size filter)
from skimage.feature import peak_local_max
from skimage.measure import label
from scipy.ndimage import distance_transform_edt
from aicssegmentation.core.seg_dot import dot_3d, dot_3d_wrapper 
from aicssegmentation.core.pre_processing_utils import intensity_normalization, image_smoothing_gaussian_slice_by_slice
from skimage.morphology import remove_small_objects, dilation, erosion, ball     # function for post-processing (size filter) removed watershed
from skimage.feature import peak_local_max
from skimage.measure import label
from scipy.ndimage import distance_transform_edt

# function for core algorithm
from aicssegmentation.core.vessel import filament_2d_wrapper,filament_3d_wrapper
from aicssegmentation.core.pre_processing_utils import intensity_normalization, image_smoothing_gaussian_3d
from aicssegmentation.core.utils import get_middle_frame, hole_filling, get_3dseed_from_mid_frame
from skimage.morphology import remove_small_objects, dilation, ball, opening, cube

input_directory = "/allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/raw/raw_test2"
output_directory = "/allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/raw/seg_vesselness"

for file in os.listdir(input_directory):
    # reading in file
    filename = os.path.join(input_directory, file)
    reader = AICSImage(filename) 
    IMG = reader.data.astype(np.float32)
    structure_channel = 0
    struct_img0 = IMG[0,structure_channel,:,:,:].copy()
    
    # pre-processing
    intensity_scaling_param = [5000] # current: [1,18]
    gaussian_smoothing_sigma = 1
    struct_img = intensity_normalization(struct_img0, scaling_param=intensity_scaling_param)
    structure_img_smooth = image_smoothing_gaussian_3d(struct_img, sigma=gaussian_smoothing_sigma)
    
    # core algorithm
    vesselness_sigma1 = [1.5] 
    vesselness_cutoff1 = 0.17
    response1 = vesselness3D(structure_img_smooth, sigmas=vesselness_sigma1,  tau=1, whiteonblack=True)
    bw1 = response1 > vesselness_cutoff1
    
    #save
    seg = bw1 >0
    out=seg.astype(np.uint8)
    out[out>0]=255
    imsave(output_directory +"/" +"SEGvesselness_" + "{}".format(file), out) # switch this to imsave
