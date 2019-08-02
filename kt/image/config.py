
import imagehash
import functools

class ImageConf(object):
    
    _VALID_IMAGE_SUFFIXES = ['png', 'jpg', 'bmp']
    _IMAGE_HASH_MODE = {
        'a': imagehash.average_hash,  # average hash
        'p': imagehash.phash,         # perception hash
        'd': imagehash.dhash,         # difference hash
        'w': imagehash.whash          # wavelet hash
    }