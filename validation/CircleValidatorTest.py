import cv2
import numpy as np
import os


def make_circle(filename):

    filename_and_path = "TestImages/" + filename
    image = cv2.imread(filename_and_path, cv2.IMREAD_COLOR)

    # Do image pre_processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform
    detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20,
                                        param1=50,
                                        param2=30,
                                        minRadius=5,
                                        maxRadius=35)

    # Draw detected circles
    if detected_circles is not None:

        print("Number of detected circles : " + str(len(detected_circles[0])))

        # Make sure we have integers
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle.
            cv2.circle(image, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(image, (a, b), 1, (0, 0, 255), 3)

        # make change here when creating new validate test set
        filename = "TestImagesValidated/param2:30,MinRadius:5/" + filename
        cv2.imwrite(filename, image)

    else:
        print("Image after HT; if we get here an image was None")

    # Use this if you want to check for the photos that are not detected. Remember to comment out line 40 + 41.
    # filename = "TestImagesValidated/param2:30,MinRadius:5/" + filename
    # cv2.imwrite(filename, image)


# Iterate through all test images in directory TestImages. 'image_file' is the name of the current file object
for image_file in os.listdir("TestImages"):
    print("Name of file: " + image_file)
    make_circle(image_file)

# Der er 599 test billeder fra Andreas. Når du tester så lav samme struktur med directories som der er i
# TestImagesValidated. Tænker hvert directory får et navn der svarer til de parametre vi har kørt billederne igennem
# validateren. Når du har kørt en test igennem kan du gå ind i den tilsvarende mappe med billeder med stifinder
# og trykke CTRL + A for at se hvor mange filer den har genereret. Antallet af filer svarer til hvor mange rigtige den
# har valideret ud af de 599. Opret en #infoFile ligesom der allerede er med dataen.