import cv2
import numpy as np


def circle_detection(input_img):
    height, width, channels = input_img.shape
    largest_dimension = max(width, height)


    # Convert to grayscale.
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred,
                                        cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                        param2=largest_dimension / 5, minRadius=0, maxRadius=0)
    # Draw circles that are detected.
    if detected_circles is not None:
        print("NUMBER OF DETECTED CIRCLES : " + str(len(detected_circles[0])))

        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle.
            cv2.circle(input_img, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(input_img, (a, b), 1, (0, 0, 255), 3)
        cv2.imshow("Detected Circle", input_img)
        cv2.waitKey(0)

    else:
        print("No circles were detected")




img = cv2.imread('C:/Users/sujee/PycharmProjects/speed-sign-recognition/validation/img/circle.jpg')

# Converts images from BGR to HSV
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_red1 = np.array([0, 50, 20])
upper_red1 = np.array([5, 255, 255])

lower_red2 = np.array([175, 50, 20])
upper_red2 = np.array([180, 255, 255])


# Here we are defining range of bluecolor in HSV
# This creates a mask of blue coloured
# objects found in the frame.
mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)

mask_res = mask1 + mask2

res = cv2.bitwise_and(img,img, mask= mask_res)
circle_detection(res)

# The bitwise and of the frame and mask is done so
# that only the blue coloured objects are highlighted
# and stored in res

"""cv2.imshow('img',img)
cv2.imshow('mask',mask_res)
cv2.imshow('res',res)
cv2.waitKey(0)"""