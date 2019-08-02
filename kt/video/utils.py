
from .config import VideoConf as VidConf

def get_video_fourcc(vid_suffix):
    """Get corresponding fourcc for opencv-python video ops
    
    Arguments:
        vid_suffix {str} -- video suffix
    
    Returns:
        str -- video fourcc or None
    """
    
    if vid_suffix in VidConf._VIDEO_FORMAT_FOURCC:
        return VidConf._VIDEO_FORMAT_FOURCC[vid_suffix]

def get_video_frame_multiplier(mode):
    """Get the multipliers corresponding different time scale
    
    Arguments:
        mode {str} -- key of time scale, [second, minute, hour]
    
    Returns:
        int -- multiplier
    """

    if mode in VidConf._VIDEO_FRAME_MULTIPLIER:
        return VidConf._VIDEO_FRAME_MULTIPLIER[mode]
