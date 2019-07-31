
from . import config as VidConf

def get_video_fourcc(vid_suffix):
    """Get corresponding fourcc for opencv-python video ops
    
    Arguments:
        vid_suffix {str} -- video suffix
    
    Returns:
        str -- video fourcc or None
    """
    
    return getattr(VidConf._VIDEO_FORMAT_FOURCC, vid_suffix, None)