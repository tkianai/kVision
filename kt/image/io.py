"""This module handles image input and output
"""

import cv2
from PIL import Image
import numpy as np

def imread(img, mode='O'):
    """read image file
    
    Arguments:
        img {path} -- image path
    
    Keyword Arguments:
        mode {str} -- image format ['np', 'pil'] (default: {'O'})
    
    Returns:
        image -- numpy ndarray or PIL data
    """

    if isinstance(img, str):
        img = cv2.imread(img)

    if mode == 'O':
        if not isinstance(img, np.ndarray):
            img = np.array(img)
    else:
        if isinstance(img, np.ndarray):
            img = Image.fromarray(img)

    return img
