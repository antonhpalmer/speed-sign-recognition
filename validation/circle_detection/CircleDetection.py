import cv2
import numpy as np


class ValidatedImage:
    def __init__(self, pil_image):
        self.img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        self.is_valid = None
        self.circle_center = None
        self.radius = None

    def __find_largest_circle(self, detected_circles):
        r = 0
        b = None
        a = None
        for pt in detected_circles[0, :]:
            if pt[2] > r:
                a, b, r = pt[0], pt[1], pt[2]

        return a, b, r


    def circle_detection(self):
        # Convert to grayscale.
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # Blur using 3 * 3 kernel.
        gray_blurred = cv2.blur(gray, (3, 3))

        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blurred,
                                            cv2.HOUGH_GRADIENT, 1, 40, param1=50,
                                            param2=30, minRadius=5, maxRadius=0)
        # Draw circles that are detected.
        if detected_circles is not None:
            self.is_valid = True

            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))

            a, b, r = self.__find_largest_circle(detected_circles)

            self.circle_center = a, b
            self.radius = r

        else:
            self.is_valid = False
