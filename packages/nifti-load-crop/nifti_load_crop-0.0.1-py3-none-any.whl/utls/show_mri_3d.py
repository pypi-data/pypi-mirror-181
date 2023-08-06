# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 23:23:58 2022

@author: pobe4699
"""
import matplotlib.pyplot as plt
from scipy import ndimage
import numpy as np


def view_slices_3d(image_3d_1, image_3d_2, slice_nbr, vmin, vmax, title=''):
    fig = plt.figure(figsize=(15, 12))
    plt.suptitle(title, fontsize=10)

    plt.subplot(231)
    image_rot = ndimage.rotate(np.take(image_3d_1, slice_nbr, 1), 90)
    plt.imshow(image_rot, vmin=vmin, vmax=vmax, cmap='gray', aspect="equal")
    plt.title('Axial');

    plt.subplot(232)
    # plt.imshow(np.take(image_3d_1, slice_nbr, 2), vmin=vmin, vmax=vmax, cmap='gray')
    image_rot = ndimage.rotate(np.take(image_3d_1, slice_nbr, 2), 0)
    plt.imshow(image_rot, vmin=vmin, vmax=vmax, cmap='gray', aspect="equal")
    plt.title('Coronal1');

    plt.subplot(233)
    image_rot = ndimage.rotate(np.take(image_3d_1, slice_nbr, 0), 90)
    plt.imshow(image_rot, vmin=vmin, vmax=vmax, cmap='gray', aspect="equal")
    plt.title('Sagittal1');
    cbar = plt.colorbar()

    plt.subplot(234)
    image_rot = ndimage.rotate(np.take(image_3d_2, slice_nbr, 1), 90)
    plt.imshow(image_rot, vmin=vmin, vmax=vmax, cmap='gray', aspect="equal")
    # plt.title('Axia2');

    plt.subplot(235)
    image_rot = ndimage.rotate(np.take(image_3d_2, slice_nbr, 2), 0)
    plt.imshow(image_rot, vmin=vmin, vmax=vmax, cmap='gray', aspect="equal")
    # plt.title('Coronal2');

    plt.subplot(236)
    image_rot = ndimage.rotate(np.take(image_3d_2, slice_nbr, 0), 90)
    plt.imshow(image_rot, vmin=vmin, vmax=vmax, cmap='gray', aspect="equal")
    # plt.title('Sagittal2');
    cbar = plt.colorbar()

    # Save as pdf

    # plt.savefig('save as dpi.pdf', dpi=120, format='pdf', bbox_inches='tight')

# ## Coronal image in focus


def coronall_slices_3d(image_3d_1, slice_nbr, vmin, vmax, title=''):
    fig = plt.figure(figsize=(15, 12))

    plt.subplot(111)
    # plt.imshow(np.take(image_3d_1, slice_nbr, 2), vmin=vmin, vmax=vmax, cmap='gray')
    image_rot = ndimage.rotate(np.take(image_3d_1, slice_nbr, 2), 270)
    plt.imshow(image_rot, vmin=vmin, vmax=vmax, cmap='gray', aspect="equal")
    plt.title('Coronal1');

