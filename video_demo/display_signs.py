import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

from validation.circle_detection.CircleDetection import ValidatedImage


def display_signs_func(detected_image, preprocessed_image, classified_sign):
    validated_image = ValidatedImage(detected_image)
    validated_image.circle_detection()
    validated_image.draw_circle("", "validated_image.png")

    preprocessed_image.save("preprocessed_image.png")

    # fig = plt.figure()pixy
    image1 = plt.subplot(221)
    image2 = plt.subplot(222)
    image3 = plt.subplot(223)
    image4 = plt.subplot(224)

    image1.set_title("Original image")
    image2.set_title("Validated image")
    image3.set_title("Preprocessed image")
    image4.set_title("Classified sign")

    img_path_to_source2 = "video_demo/speedsign" + str(classified_sign) + ".png"
    img_source1 = mpimg.imread('out.ppm')
    img_source2 = mpimg.imread('validated_image.png')
    img_source3 = mpimg.imread('preprocessed_image.png')
    img_source4 = mpimg.imread(img_path_to_source2)

    _ = image1.imshow(img_source1)
    _ = image2.imshow(img_source2)
    _ = image3.imshow(img_source3, cmap='Greys_r')
    _ = image4.imshow(img_source4)

    image1.axis("off")
    image2.axis("off")
    image3.axis("off")
    image4.axis("off")
    plt.show()
