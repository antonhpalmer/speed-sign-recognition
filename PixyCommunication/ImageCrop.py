from PIL import Image


def crop_image(path, x1, y1, x2, y2):
    image_object = Image.open(path)

    cropped = image_object.crop((x1, y1, x2, y2))

    cropped.save("cropped.ppm")


crop_image('out.ppm', 1, 1, 100, 100)
