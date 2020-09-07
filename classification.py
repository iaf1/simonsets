import cv2
import matplotlib.pyplot as plt
import numpy as np
from correlation_functions import correlate, binarize

img = cv2.imread('test_image.jfif')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to gray scale


# COLOR DETECTION

# Then we define the color thresholds in the HSV space

low_red = np.array([161, 50, 50])
high_red = np.array([179, 255, 255])
low_red_1 = np.array([0, 0, 0])
high_red_1 = np.array([10, 255, 255])
red_mask = np.logical_or(cv2.inRange(img_hsv, low_red, high_red), cv2.inRange(img_hsv, low_red_1, high_red_1)).astype(int)

low_green = np.array([40, 100, 100])
high_green = np.array([90, 255, 255])
green_mask = cv2.inRange(img_hsv, low_green, high_green)/255

low_blue = np.array([110, 100, 50])
high_blue = np.array([130, 255, 255])
blue_mask = cv2.inRange(img_hsv, low_blue, high_blue)/255

# We detect the color of the card

color_masks = np.array((red_mask, green_mask, blue_mask))
sum_pix = np.sum(color_masks, axis=2)
color_index = np.where(sum_pix == np.amax(sum_pix))[0][0]
colors = ['Red', 'Green', 'Blue']

print('The card is color ' + str(colors[color_index]))

# FILLING DETECTION

# We blur the gray image

blurred_img = cv2.blur(img_gray, (2, 2))

# We apply a Canny edge detector

edges = cv2.Canny(blurred_img, 200, 500)

contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

mask = np.zeros_like(img[:, :, 0])
cv2.drawContours(mask, contours[1], -1, 1, -1)

contour_img = np.zeros_like(img[:, :, 0])
cv2.drawContours(contour_img, contours[1], -1, 1, 1)

filling = 100 - (np.sum(mask) - np.sum(color_masks[color_index]))*100/(np.sum(mask) - np.sum(contour_img))

if filling < 10:
    print('The figure is not filled')
elif filling >= 10 and filling <= 95:
    print('The figure is partially filled')
elif filling > 90:
    print('The figure is completely filled')

"""fig, ax = plt.subplots(2, 2)
ax[0][0].imshow(img_rgb)
ax[0][1].imshow(contour_img)
ax[1][0].imshow(mask)
ax[1][1].imshow(green_mask)
plt.show()"""

# SHAPE DETECTION

img_bin = binarize(img_gray)

elipse = cv2.imread('elipse.jpg', cv2.IMREAD_GRAYSCALE)
rectangle = cv2.imread('rectangle.jpg', cv2.IMREAD_GRAYSCALE)
wave = cv2.imread('onada.jpg', cv2.IMREAD_GRAYSCALE)

elipse_idx = correlate(img_gray, elipse).max()
rectangle_idx = correlate(img_gray, rectangle).max()
wave_idx = correlate(img_gray, wave).max()

fig, ax = plt.subplots(2, 2)
ax[0][0].imshow(elipse_idx)
ax[0][1].imshow(rectangle_idx)
ax[1][0].imshow(wave_idx)
ax[1][1].imshow(img)
plt.show()