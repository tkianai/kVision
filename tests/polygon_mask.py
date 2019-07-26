
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

def parse_args():

    parser = argparse.ArgumentParser(description="Test polygon mask transformation")
    parser.add_argument('--mask')
    parser.add_argument('--save', default='./work_dirs/generated/')

    args = parser.parse_args()
    if not os.path.exists(args.save):
        os.makedirs(args.save)
    return args


def main(args):
    
    # transform with skimage module
    # NOTE multipart type succeeded, border_type failed
    mask = Image.open(args.mask)
    mask = np.array(mask)
    polygons = measure.find_contours(mask.astype(np.float), 0.5)
    reconstruct_mask = np.zeros(mask.shape)
    for polygon in polygons:
        reconstruct_mask += polygon2mask(mask.shape, polygon)
    reconstruct_mask = reconstruct_mask.astype(np.bool)
    reconstruct_mask = Image.fromarray(reconstruct_mask)
    reconstruct_mask.save(os.path.join(args.save, "reconstructed_mask_skim.png"))

    # transform with cv2
    # NOTE both succeeded
    mask = cv2.imread(args.mask)
    if len(mask.shape) == 3:
        mask = mask[:, :, 0]

    mask = cv2.copyMakeBorder(mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    polygons = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE, offset=(-1, -1))
    polygons = polygons[0] if len(polygons) == 2 else polygons[1]
    polygons = [polygon.flatten() for polygon in polygons]

    reconstruct_mask = np.zeros(mask.shape)
    for polygon in polygons:
        polygon = polygon.reshape(-1, 2)[:, ::-1]
        reconstruct_mask += polygon2mask(mask.shape, polygon)
    reconstruct_mask = reconstruct_mask.astype(np.bool) * 255
    # NOTE you can save with cv2.imwrite, donot care about the data dtype, while the data scale must range from 0 to 255. When load image with cv2.imread, the image data scale range from 0 to 255, dtype equals to np.uint8, and the image channel is set to default with BGR.
    cv2.imwrite(os.path.join(args.save, "reconstructed_mask_cv.png"), reconstruct_mask)
    

if __name__ == "__main__":
    args = parse_args()
    main(args)
