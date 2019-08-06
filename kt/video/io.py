
"""This provides video io operations

> write_imgs2vid
> extract_vid2imgs
"""

import os
import cv2
import time
import shutil
from kt.image import image_format_check
from kt.video import get_video_fourcc
from kt.video import get_video_frame_multiplier

def write_imgs2vid(
    save_path,
    img_dir=None,
    images=None,
    fps=25, 
    suffix='mp4',  
    start_idx=None, 
    end_idx=None,
    walk_mode=False,
):
    """Write images to video
    
    Arguments:
        save_path {path} -- video path to be saved
    
    Keyword Arguments:
        img_dir {path} -- image directory (default: {None})
        images {list} -- list of image paths (default: {None})
        fps {int} -- video frames per second (default: {25})
        suffix {str} -- video type (default: {'mp4'})
        start_idx {int} -- images start index (default: {None})
        end_idx {int} -- images end index (default: {None})
        walk_mode {bool} -- using os.walk or os.listdir (default: {False})
    """

    if images is None:
        if walk_mode:
            images = []
            for root, _, files in os.walk(img_dir):
                for file in files:
                    if image_format_check(file):
                        images.append(os.path.join(root, file))
        else:
            images = sorted(os.listdir(img_dir))
            images = [os.path.join(img_dir, e) for e in images if image_format_check(e)]
    
    sample = cv2.imread(images[0])
    if len(sample.shape) == 3:
        height, width, _ = sample.shape
    else:
        height, width = sample.shape

    save_dir = os.path.dirname(save_path)
    basename = os.path.basename(save_path)
    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
        except:
            pass
    
    if len(basename.split('.')) > 1:
        _suffix = basename.split('.')[-1]
        if get_video_fourcc(_suffix) is not None:
            suffix = _suffix
            save_name = save_path
    else:
        save_name = os.path.join(save_dir, basename + '.' + suffix)

    size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*get_video_fourcc(suffix))
    vWriter = cv2.VideoWriter(save_name, fourcc, int(fps), size)

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


def extract_vid2imgs(
    vid_path, 
    save_dir=None, 
    suffix='png',
    start_idx=None,
    end_idx=None,
    mode=None,
):
    """extract video into images
    
    Arguments:
        vid_path {path} -- video path
    
    Keyword Arguments:
        save_dir {path} -- save directory (default: {None})
        suffix {str} -- image format (default: {'png'})
        start_idx {int} -- start index (default: {None})
        end_idx {int} -- end index (default: {None})
        mode {str} -- time scale ['second', 'minute', 'hour', None] (default: {None})
    """

    if not save_dir:
        base_dir = os.path.dirname(vid_path)
        save_dir = os.path.join(base_dir, os.path.basename(vid_path).split('.')[0] + "_extracted_images")

    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
        except :
            pass

    multiplier = get_video_frame_multiplier(mode)
    vCapturer = cv2.VideoCapture(vid_path)
    total_frames = vCapturer.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = vCapturer.get(cv2.CAP_PROP_FPS)
    height = vCapturer.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vCapturer.get(cv2.CAP_PROP_FRAME_WIDTH)

    # sanity check
    if start_idx is None:
        start_idx = 0
    if end_idx is None:
        end_idx = total_frames

    # update start index and end index
    if multiplier:
        start_idx *= multiplier * fps
        end_idx *= multiplier * fps
    
    start_idx = int(start_idx)
    end_idx = int(end_idx)
    start_idx = max(0, start_idx)
    end_idx = min(end_idx, total_frames)

    for i in range(start_idx):
        ret, frame = vCapturer.read()

    for i in range(start_idx, end_idx):
        ret, frame = vCapturer.read()
        save_name = os.path.join(save_dir, "{:0>10}.{}".format(i, suffix))
        cv2.imwrite(save_name, frame)

    vCapturer.release()


def extract_part_video(
    vid_path,
    save_path=None,
    fps=None,
    suffix='mp4',
    start_idx=None,
    end_idx=None,
    mode=None,
    reverse=False,
):
    """extract part of video
    
    Arguments:
        vid_path {path} -- video path
    
    Keyword Arguments:
        save_path {path} -- the video to be saved path (default: {None})
        fps {int} -- frame per second (default: {None})
        suffix {str} -- video suffix (default: {'mp4'})
        start_idx {int} -- start index (default: {None})
        end_idx {int} -- end index (default: {None})
        mode {str} -- time scale [second, minute, hour, other] (default: {None})
        reverse {bool} -- Need to be reverted (default: {False})
    """

    if not save_path:
        save_dir = os.path.dirname(vid_path)
        save_path = os.path.join(save_dir, '.'.join(os.path.basename(vid_path).split('.')[:-1]) + '_part.' + suffix)
    else:
        save_dir = os.path.dirname(save_path)

    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
        except:
            pass

    multiplier = get_video_frame_multiplier(mode)
    vCapturer = cv2.VideoCapture(vid_path)
    total_frames = vCapturer.get(cv2.CAP_PROP_FRAME_COUNT)
    orgin_fps = vCapturer.get(cv2.CAP_PROP_FPS)
    height = vCapturer.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vCapturer.get(cv2.CAP_PROP_FRAME_WIDTH)

    # sanity check
    if start_idx is None:
        start_idx = 0
    if end_idx is None:
        end_idx = total_frames

    # update start index and end index
    if multiplier:
        start_idx *= (multiplier * orgin_fps)
        end_idx *= (multiplier * orgin_fps)

    start_idx = int(start_idx)
    end_idx = int(end_idx)
    start_idx = max(0, start_idx)
    end_idx = min(end_idx, total_frames)

    size = (int(width), int(height))
    if fps is None:
        fps = orgin_fps

    fourcc = cv2.VideoWriter_fourcc(*get_video_fourcc(suffix))
    vWriter = cv2.VideoWriter(save_path, fourcc, int(fps), size)

    for i in range(start_idx):
        ret, frame = vCapturer.read()

    if reverse:
        temp_dir = os.path.join(save_dir, str(time.time()))
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        for i in range(start_idx, end_idx):
            ret, frame = vCapturer.read()
            cv2.imwrite(os.path.join(temp_dir, "{:0>10}.png".format(i)), frame)

        images = os.listdir(temp_dir)
        images = sorted(images, reverse=True)
        for image in images:
            img = cv2.imread(os.path.join(temp_dir, image))
            vWriter.write(img)

        shutil.rmtree(temp_dir)
    else:
        for i in range(start_idx, end_idx):
            ret, frame = vCapturer.read()
            vWriter.write(frame)

    vCapturer.release()
    vWriter.release()
