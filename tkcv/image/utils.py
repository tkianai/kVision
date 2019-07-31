
from . import config as ImgConf
import os

def image_format_check(img_path):
    """This check the image path whether legal or not
    
    Arguments:
        img_path {path} -- image path
    
    Returns:
        bool -- if it is a valid image file, return True.
    """
    
    suffix = img_path.split('.')[-1]
    if suffix in ImgConf._VALID_IMAGE_SUFFIXES:
        return True
    
    return False

