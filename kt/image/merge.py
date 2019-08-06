"""This module handle ops between several images
"""

import cv2
from kt.image import imread

def make_overlay(background, images=None, masks=None, threshold=128, reverse=False, ratio=1.0):
    """This creates overlayed images
    
    Arguments:
        background {path} -- the image to be overlayed
    
    Keyword Arguments:
        images {list} -- list of image paths (default: {None})
        masks {list} -- list of corresponding mask (default: {None})
        threshold {int} -- threshold to compute bool mask (default: {128})
        reverse {bool} -- whether reverse the selected region or not (default: {False})
        ratio {float} -- merge ratio (default: {1.0})
    
    Returns:
        numpy array -- H X W X C
    """

    if masks is not None:
        assert len(images) == len(masks), "the length of images must be equal to masks"

    base = imread(background)
    for i, image in enumerate(images):
        img = imread(image)
        if masks is not None:
            mask = imread(masks[i])
            if len(mask.shape) == 3:
                mask = mask[:, :, 0]
        else:
            mask = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        if reverse:
            mask = mask < threshold
        else:
            mask = mask > threshold

        base[mask, :] = base[mask, :] * (1 - ratio) + img[mask, :] * ratio
    return base.astype(np.uint8)
