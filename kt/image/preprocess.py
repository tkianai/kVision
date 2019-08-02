"""This module includes some image preprocessing functions
"""

import os
import cv2
from PIL import Image
import numpy as np
from .config import ImageConf as ImgConf

def is_blurry_by_gradient(img, threshold=None):
    """This detects whether image is blurry or not by laplacian
    
    Arguments:
        img {numpy array} -- H x W X 3
    
    Keyword Arguments:
        threshold {float} -- gradient var (default: {None})
    
    Returns:
        bool -- whether blurry or not
    """

    if isinstance(img, str):
        img = cv2.imread(img)
    if threshold is None:
        threshold = img.shape[0] * img.shape[1] * 0.01

    return cv2.Laplacian(img, cv2.CV_64F).var() > threshold


def get_image_hashcode(img, mode='a', hash_size=8, **kwargs):
    """This returns image hash code
    
    Arguments:
        img {PIL image} -- PIL style image
    
    Keyword Arguments:
        mode {str} -- [a, p, d, w] (default: {'a'})
        hash_size {int} -- image size to resize (default: {8})
        kwargs {} -- highfreq_factor related to mode(p)
    
    Returns:
        [type] -- [description]
    """

    if isinstance(img, str):
        img = Image.open(img)
    elif isinstance(img, np.ndarray):
        img = Image.fromarray(img)

    hashcode = None
    if mode in ImgConf._IMAGE_HASH_MODE:
        hashcode = ImgConf._IMAGE_HASH_MODE[mode](img, hash_size=hash_size, **kwargs)
        hashcode = str(hashcode)

    return hashcode
