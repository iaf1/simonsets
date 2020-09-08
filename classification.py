import cv2
import matplotlib.pyplot as plt
import numpy as np
from correlation_functions import correlate, binarize

def classification(img_bgr):
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)  # convert to gray scale

    # COLOR DETECTION

    # We define the color thresholds in the HSV space
    low_red = np.array([161, 30, 30])
    high_red = np.array([179, 255, 255])
    low_red_1 = np.array([0, 30, 30])
    high_red_1 = np.array([10, 255, 255])
    red_mask = np.logical_or(cv2.inRange(img_hsv, low_red, high_red), cv2.inRange(img_hsv, low_red_1, high_red_1)).astype(int)

    low_green = np.array([40, 30, 30])
    high_green = np.array([90, 255, 255])
    green_mask = cv2.inRange(img_hsv, low_green, high_green)/255

    low_blue = np.array([110, 50, 50])
    high_blue = np.array([130, 255, 255])
    blue_mask = cv2.inRange(img_hsv, low_blue, high_blue)/255

    color_masks = np.array((red_mask, green_mask, blue_mask))
    sum_pix = np.sum(color_masks, axis=2)
    color_index = np.where(sum_pix == np.amax(sum_pix))[0][0]

    # FILLING DETECTION

    # We blur the gray image

    blurred_img = cv2.blur(img_gray, (2, 2))

    # We apply a Canny edge detector

    edges = cv2.Canny(blurred_img, 200, 500)

    contours = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    good_contours = np.where(contours[1][:, :, 3][0] == 1)

    mask = np.zeros_like(img_bgr[:, :, 0])
    for i in range(len(good_contours[0])):
        cv2.drawContours(mask, contours[0], good_contours[0][i], 1, -1)

    contour_img = np.zeros_like(img_bgr[:, :, 0])
    for i in range(len(good_contours[0])):
        cv2.drawContours(contour_img, contours[0], good_contours[0][i], 1, 1)

    filling = 100 - (np.sum(mask) - np.sum(color_masks[color_index]))*100/(np.sum(mask) - np.sum(contour_img)*6)

    if filling < 5:
        filling_idx = 0
    elif filling >= 5 and filling <= 90:
        filling_idx = 1
    elif filling > 90:
        filling_idx = 2

    # SHAPE DETECTION

# =============================================================================
# ALBERT'S IMPLEMENTATION
# =============================================================================
#     elipse = cv2.imread('elipse.jpg', cv2.IMREAD_GRAYSCALE)
#     rectangle = cv2.imread('rectangle.jpg', cv2.IMREAD_GRAYSCALE)
#     wave = cv2.imread('onada.jpg', cv2.IMREAD_GRAYSCALE)
# 
#     elipse_idx = correlate(contour_img, elipse).max()
#     rectangle_idx = correlate(contour_img, rectangle).max()
#     wave_idx = correlate(contour_img, wave).max()
# 
#     shapes = np.array((elipse_idx, wave_idx, rectangle_idx))
#     shape_index = np.where(shapes == np.amax(shapes))[0][0]
# =============================================================================
    
    blank = np.zeros_like(img_bgr[:,:,0])
    ellipse = cv2.fitEllipse(contours[0][0])
    ellipse_im = cv2.ellipse(blank, ellipse, 255, 2)
    ellipse_cont = cv2.findContours(ellipse)

    # NUMBER DETECTION

    number = len(good_contours[0])

    return number, shape_index + 1, color_index + 1, filling_idx + 1