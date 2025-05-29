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
from skimage.morphology import remove_small_objects, dilation, erosion, ball     # function for post-processing (size filter)
from skimage.feature import peak_local_max
from skimage.measure import label
from scipy.ndimage import distance_transform_edt

# function for core algorithm
from aicssegmentation.core.vessel import filament_2d_wrapper,filament_3d_wrapper
from aicssegmentation.core.pre_processing_utils import intensity_normalization, image_smoothing_gaussian_3d
from aicssegmentation.core.utils import get_middle_frame, hole_filling, get_3dseed_from_mid_frame
from skimage.morphology import remove_small_objects, dilation, ball, opening, cube

# input directories
vesselness_input = "/allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/seg/seg_vesselness"
laminshell_input = "/allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/seg/seg_laminshell"

# output directories to save to 
intersection_output = "/allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/seg/seg_intersection"
finalspeckle_output = "/allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/seg/seg_finalspeckle"

for i in range(0,530):
    
    # folders to iterate through
    laminshell_folder = os.listdir(laminshell_input)
    vesselness_folder = os.listdir(vesselness_input)

    structure_channel = 0

    # read in lamin shell file 
    filename_lamin = os.path.join(laminshell_input, laminshell_folder[i])
    reader_lamin = AICSImage(filename_lamin) 
    lamin = reader_lamin.data.astype(np.uint8)
    struct_lamin = lamin[0,structure_channel,:,:,:].copy()

    # read in vesselness file 
    filename_vesselness = os.path.join(vesselness_input, vesselness_folder[i])
    reader_vesselness = AICSImage(filename_vesselness) 
    speckle = reader_vesselness.data.astype(np.uint8)
    struct_speckle = speckle[0,structure_channel,:,:,:].copy()

    print("lamin:", filename_lamin)
    print("speckle:", filename_vesselness)

    # get the intersection between speckle and lamin shell segmentation
    intersection = speckle & lamin
 
    # subtract intersection from speckle segmentation
    subtracted = speckle - intersection
    
    # save intersection segmentation 
    imsave(intersection_output +"/" +"SEGintersection_" + "{}".format(laminshell_folder[i].split('_')[-1]), intersection)
    
    # save intersection segmentation 
    imsave(finalspeckle_output +"/" +"SEGfinalspeckle_" + "{}".format(vesselness_folder[i].split('_')[-1]), subtracted)
    
    print("DONE")

    # save intersection segmentation 
    #     imsave(intersection_output +"/" +"SEGintersection_" + "{}".format(file_lamin), intersection)

    #     # subtract intersection from speckle segmentation
    #     subtracted = speckle - intersection

    #     # save intersection segmentation 
    #     imsave(finalspeckle_output +"/" +"SEGfinalspeckle_" + "{}".format(file_lamin), subtracted)

    print("DONE")

# for file_lamin in os.listdir(laminshell_input):
#     for file_vesselness in os.listdir(vesselness_input):
#         structure_channel = 0
#         # read in vesselness folder
      
#         filename_lamin = os.path.join(laminshell_input, file_lamin)
#         reader_lamin = AICSImage(filename_lamin) 
#         lamin = reader_lamin.data.astype(np.uint8)
#         struct_lamin = lamin[0,structure_channel,:,:,:].copy()

#         # reading in file
#         filename_vesselness = os.path.join(vesselness_input, file_vesselness)
#         reader_vesselness = AICSImage(filename_vesselness) 
#         speckle = reader_vesselness.data.astype(np.float32)
#         struct_speckle = speckle[0,structure_channel,:,:,:].copy()

#         print("lamin:", file_lamin)
#         print("speckle:", file_vesselness)

#         print("DONE.")

    # for file_vesselness in os.listdir(vesselness_input):
    #     structure_channel = 0

        
   



    #     # get the intersection between speckle and lamin shell segmentation
    #     intersection = speckle + lamin
  

    #     # save intersection segmentation 
    #     imsave(intersection_output +"/" +"SEGintersection_" + "{}".format(file_lamin), intersection)

    #     # subtract intersection from speckle segmentation
    #     subtracted = speckle - intersection

    #     # save intersection segmentation 
    #     imsave(finalspeckle_output +"/" +"SEGfinalspeckle_" + "{}".format(file_lamin), subtracted)

    #     print("DONE.")

