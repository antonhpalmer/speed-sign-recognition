import cv2
import numpy as np

# Read image.
input_img = cv2.imread('C:/Users/sujee/PycharmProjects/speed-sign-recognition/test_data/training_images/30/grouproom_floor_light107.ppm', cv2.IMREAD_COLOR)
img = input_img[10:80, 10:76]
dest_path = 'C:/Users/sujee/PycharmProjects/speed-sign-recognition/validation/img/different_image_transformations/'
img = cv2.resize(img,(164,172))
cv2.imwrite(dest_path + 'input2.jpg', img)
# Convert to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(dest_path + 'grayscale2.jpg', gray)

# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (3, 3))
cv2.imwrite(dest_path + 'grayblurred2.jpg', gray_blurred)

# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(gray_blurred,
                                    cv2.HOUGH_GRADIENT, 1, 14, param1=90,
                                    param2=27, minRadius=9, maxRadius=0)
# Draw circles that are detected.
if detected_circles is not None:

    r_max = 0
    b_max = None
    a_max = None
    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
        r_max, a_max, b_max = r, a, b

    if r_max == 0:
        r_max = None

    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))

    a, b, r = a_max, b_max, r_max

    # Draw the circumference of the circle.
    cv2.circle(img, (a, b), r, (0, 255, 0), 2)

    # Draw a small circle (of radius 1) to show the center.
    cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
    #cv2.imshow("Detected Circle", img)
    cv2.imwrite(dest_path + 'circle2.ppm', img)