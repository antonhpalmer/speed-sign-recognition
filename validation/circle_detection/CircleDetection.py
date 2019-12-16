import cv2
import numpy as np
import math
from validation.circle_detection.extract_red_from_image import filter_red as red


class ValidatedImage:
    def __init__(self, pil_image):
        self.img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        self.red_img = cv2.cvtColor(np.array(red(pil_image)), cv2.COLOR_RGB2BGR)
        self.is_valid = None
        self.circle_center = None
        self.radius = None

    #Checks whether the inputted circle fits within the picture
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
        self.circle_detection_with_params(6, 52, 26, 8, 0)


    def circle_detection_with_params(self, min_distance, param1, param2, min_radius, max_radius):
        # Convert image to grayscale.
        gray = cv2.cvtColor(self.red_img, cv2.COLOR_BGR2GRAY)

        # Blur using a 3 * 3 kernel.
        gray_blurred = cv2.blur(gray, (3, 3))



        height, width, channels = self.img.shape
        half_max_dim = math.ceil(max(height, width) / 2)

        # Apply Hough Transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blurred,
                                            cv2.HOUGH_GRADIENT, 1, min_distance, param1=param1,
                                            param2=param2, minRadius=min_radius, maxRadius=half_max_dim)

        if detected_circles is not None:

            # Convert the parameters a, b and r to integers
            detected_circles = np.uint16(np.around(detected_circles))

            a, b, r = self.__find_largest_circle_within_image(detected_circles)

            if r is not None and (a, b) is not None:
                self.is_valid = True
                self.circle_center = a, b
                self.radius = r
            else:
                self.is_valid = False
        else:
            self.is_valid = False

    def draw_circle(self, dest_path, file_name):
        # Draw the circle.
        if self.radius is not None and self.circle_center is not None:
            cv2.circle(self.img, self.circle_center, self.radius, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(self.img, self.circle_center, 1, (0, 0, 255), 3)

            cv2.imwrite(dest_path + file_name, self.img)

        else:
            cv2.imwrite(dest_path + file_name, self.red_img)