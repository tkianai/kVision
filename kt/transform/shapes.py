

import os
import cv2
import argparse
import numpy as np
from skimage import measure
from skimage import draw
from PIL import Image


def polygon2mask(image_shape, polygon):
    """Compute a mask from polygon.
    Parameters
    ----------
    image_shape : tuple of size 2.
        The shape of the mask.
    polygon : array_like.
        The polygon coordinates of shape (N, 2) where N is
        the number of points.
    Returns
    -------
    mask : 2-D ndarray of type 'bool'.
        The mask that corresponds to the input polygon.
    Notes
    -----
    This function does not do any border checking, so that all
    the vertices need to be within the given shape.
    Examples
    --------
    >>> image_shape = (128, 128)
    >>> polygon = np.array([[60, 100], [100, 40], [40, 40]])
    >>> mask = polygon2mask(image_shape, polygon)
    >>> mask.shape
    (128, 128)
    """
    polygon = np.asarray(polygon)
    vertex_row_coords, vertex_col_coords = polygon.T
    fill_row_coords, fill_col_coords = draw.polygon(
        vertex_row_coords, vertex_col_coords, image_shape)
    mask = np.zeros(image_shape, dtype=np.bool)
    mask[fill_row_coords, fill_col_coords] = True
    return mask


def mask2polygon(mask):
    """Transfer binaray mask into polygons 
    
    Arguments:
        mask {numpy array} -- H x W X C
    
    Returns:
        list -- each element stands for one polygon(numpy array, N x 2)
    """

    if len(mask.shape) == 3:
        mask = mask[:, :, 0]

    mask = cv2.copyMakeBorder(mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    polygons = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE, offset=(-1, -1))
    polygons = polygons[0] if len(polygons) == 2 else polygons[1]
    polygons = [polygon.flatten().reshape(-1, 2)[:, ::-1] for polygon in polygons]

    return polygons
