import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image


def display_signs_func(pixy_image, classified_sign):

    # Saving ppm input image as png for the matplotlib to work properly
    pixy_image = Image.open(pixy_image)
    pixy_image.save("pixy_image.png")

    fig = plt.figure()
    image1 = plt.subplot(121)
    image2 = plt.subplot(122)

    img_path_to_source2 = "speedsign" + str(classified_sign) + ".png"
    img_source1 = mpimg.imread('pixy_image.png')
    img_source2 = mpimg.imread(img_path_to_source2)

    _ = image1.imshow(img_source1)
    _ = image2.imshow(img_source2)

    image1.axis("off")
    image2.axis("off")
    plt.show()

