"""This visualize the keypoints, including pose, face, hand and so on
"""


import os
import cv2
import numpy as np


def show_keypoints_over_image(
    img, 
    points, 
    skeletons=None,
    point_radius=3,
    point_color=(0, 255, 0),
    line_width=2,
    line_color=None,
):
    """Plot keypoints on image
    
    Arguments:
        img {str | np img | pil img} -- input image
        points {list of list} -- point set
    
    Keyword Arguments:
        skeletons {list of list} -- point collection (default: {None})
        point_radius {int} -- radius of keypoint (default: {3})
        point_color {tuple} -- keypoint color to show (default: {(0, 255, 0)})
        line_width {int} -- line width(default: {2})
        line_color {tuple} -- line color to show (default: {None})
    
    Returns:
        img -- numpy image[opencv]
    """

    if isinstance(img, str):
        img = cv2.imread(img)

    if isinstance(img, np.ndarray):
        img = np.array(img)   # Handle PIL object

    # plot isolate keypoints
    for point in points:
        # point: [width(x), height(y), visible]
        if point[2] > 0:
            img = cv2.circle(img, (int(point[0]), int(point[1])), point_radius, point_color,-1)
    
    
    # plot skeletons
    if skeletons is not None:
        for skeleton in skeletons:
            for i in range(len(skeleton) - 1):

                p1_v, p2_v = points[skeleton[i]][2], points[skeleton[i + 1]][2]
                if p1_v > 0 and p2_v > 0:
                    if line_color is None:
                        _line_color = np.random.randint(256, size=3).tolist()
                    else:
                        _line_color = line_color
                    p1 = (int(points[skeleton[i]][0]), int(points[skeleton[i]][1]))
                    p2 = (int(points[skeleton[i + 1]][0]), int(points[skeleton[i + 1]][1]))
                    img = cv2.line(img, p1, p2, _line_color, line_width)

    return img
