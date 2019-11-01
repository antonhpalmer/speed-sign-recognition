import cv2
import numpy as np


class ValidatedImage:
    def __init__(self, pil_image):
        self.img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        self.is_valid = None
        self.circle_center = None
        self.radius = None

    def __is_inside_image(self, a, b, r):
        height, width, channels = self.img.shape
        a = int(a)
        b = int(b)
        r = int(r)

        if (a - r) < 0 or (a + r) > width or (b - r) < 0 or (b + r) > height:
            return False
        else:
            return True

    def __find_largest_circle_within_image(self, detected_circles):
        r_max = 0
        b_max = None
        a_max = None
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            if self.__is_inside_image(a, b, r) and r > r_max:

                r_max, a_max, b_max = r, a, b

        if r_max == 0:
            r_max = None
        return a_max, b_max, r_max

    def circle_detection(self):
        # Convert to grayscale.
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # Blur using 3 * 3 kernel.
        gray_blurred = cv2.blur(gray, (3, 3))

        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blurred,
                                            cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                            param2=30, minRadius=10, maxRadius=0)
        # Draw circles that are detected.
        if detected_circles is not None:

            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))

            a, b, r = self.__find_largest_circle_within_image(detected_circles)

            if r is not None and (a,b) is not None:
                self.is_valid = True
                self.circle_center = a, b
                self.radius = r
            else:
                self.is_valid = False

    def draw_circle(self, dest_path, file_name):
        # Draw the circumference of the circle.
        if self.radius is not None and self.circle_center is not None:
            cv2.circle(self.img, self.circle_center, self.radius, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(self.img, self.circle_center, 1, (0, 0, 255), 3)

            cv2.imwrite(dest_path + file_name, self.img)
