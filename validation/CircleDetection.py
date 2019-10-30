import cv2
import numpy as np

# Read image.
img = cv2.imread('img/Speed60.jpg', cv2.IMREAD_COLOR)
height, width, channels = img.shape
largest_dimension = max(width, height)

print(str(height) + "," + str(width))

# Convert to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (3, 3))

# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(gray_blurred,
                                    cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                    param2=largest_dimension / 3, minRadius=0, maxRadius=0)
# Draw circles that are detected.
if detected_circles is not None:
    print("NUMBER OF DETECTED CIRCLES : " + str(len(detected_circles[0])))

    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]

        # Draw the circumference of the circle.
        cv2.circle(img, (a, b), r, (0, 255, 0), 2)

        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
    cv2.imshow("Detected Circle", img)
    cv2.waitKey(0)

else:
    cv2.imshow("Gray", gray)
    cv2.waitKey(0)
    print("No circles were detected")