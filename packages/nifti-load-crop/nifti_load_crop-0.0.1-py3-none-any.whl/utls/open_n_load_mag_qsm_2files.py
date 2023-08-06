# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 23:22:03 2022

@author: pobe4699
"""


import os
import glob
import pandas as pd

from tkinter import filedialog
from tkinter import *

import numpy as np
# import raster_geometry.raster as raster
import matplotlib.pyplot as plt

from scipy import ndimage
import math
import cv2
# TKD QSM reconstruction

import nibabel as nib
import numpy as np
from matplotlib import transforms
from scipy import ndimage
import pickle

from my_func_21 import *
selected_filter = skfilt.threshold_mean

from matplotlib.widgets import RectangleSelector
from skimage.measure import label, regionprops, regionprops_table

from skimage.filters import try_all_threshold 
import skimage.filters as skfilt
import skimage.measure as skmeas


from skimage.filters import threshold_otsu, threshold_local


# filtering_string= 'mag_MEGRE'

def open_multi_file_full_path(file_extension):  # path_to_data,
    # inputs:
    # path to file is provided either directly or by using tkinter
    # file extention of interest cvs json etc..

    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    path_to_data = folder_selected
    # get data file names, all the file extention
    path = path_to_data
    os.chdir(path)
    all_fNames0 = glob.glob(path + '/**/*.{}'.format(file_extension), recursive=True)
    print("Total number of file:", len(all_fNames0))
    # add simple filter in the string e.g. *mag_MEGRE multi echo & mag_T2starw for single twopass_average
    all_mag_fNames = glob.glob(path + '/**/*mag_MEGRE.{}'.format(file_extension), recursive=True)
    all_qsm_fNames = glob.glob(path + '/**/*scaled_qsm_000_twopass_average.{}'.format(file_extension), recursive=True)

    # print(all_fNames)

    return all_mag_fNames, all_qsm_fNames

#print ("Selected for further anlysis:",len(all_filtered_fNames_full_path))



def load2corresponding_files(path,i):  # open the files

    number_of_files = len(path)
    # print(number_of_files)
    half_num_of_files = int(number_of_files / 2)

    file_num_t1 = list(range(0, half_num_of_files))
    file_num_t2 = list(range(half_num_of_files, number_of_files))
    # %
    # for i in range (len(file_num_t1)):
    i = i
    j = i + 1
    print(i)
    wanted_1st_fNum = file_num_t1[i]
    wanted_2nd_fNum = file_num_t2[j]

    file1 = nib.load(path[wanted_1st_fNum]).get_fdata()
    print(path[wanted_1st_fNum][19:])

    file2 = nib.load(path[wanted_2nd_fNum]).get_fdata()
    print(path[wanted_2nd_fNum][19:])

    return file1, file2

