
"""This provides video io operations

> write_imgs2vid
"""

import os
import cv2
from tkcv.image import image_format_check
from tkcv.video import get_video_fourcc

def write_imgs2vid(img_dir, fps=25, suffix='mp4', save_dir=None, start_idx=None, end_idx=None):
    """Write images to video
    
    Arguments:
        img_dir {path} -- image directory
    
    Keyword Arguments:
        fps {int} -- video frames per second (default: {25})
        suffix {str} -- video type (default: {'mp4'})
        save_dir {path} -- the directory which video to be saved (default: {None})
        start_idx {int} -- images start index (default: {None})
        end_idx {int} -- images end index (default: {None})
    """

    images = sorted(os.listdir(img_dir))
    images = [os.path.join(img_dir, e) for e in images if image_format_check(e)]
    sample = cv2.imread(images[0])
    if len(sample.shape) == 3:
        height, width, _ = sample.shape
    else:
        height, width = sample.shape

    size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*get_video_fourcc(suffix))
    if not save_dir:
        save_dir = os.path.dirname(img_dir)
    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
        except :
            pass
    save_name = os.path.join(_dir, os.path.basename(img_dir) + '.' + suffix)
    vWriter = cv2.VideoWriter(save_name, fourcc, fps, size)

    if not start_idx:
        start_idx = 0
    if not end_idx:
        end_idx = len(images)

    start_idx = max(0, start_idx)
    end_idx = min(end_idx, len(images))

    for i in range(start_idx, end_idx):
        img = cv2.imread(images[i])
        vWriter.write(img)

    vWriter.release()
