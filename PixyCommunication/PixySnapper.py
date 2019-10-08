from PIL import Image
import subprocess


class PixySnapper:
    def snap_image(self):
        subprocess.call(['./get_raw_frame'])

    def crop_image(self, path, x1, y1, x2, y2):
        Image.open(path).crop((x1, y1, x2, y2)).save("cropped.ppm")

    def get_cropped_image(self, x, y, width, height):
        self.snap_image()
        self.crop_image("out.ppm", x, y, x + width, y + height)


# THIS IS A TEST OF THE CLASS
snapper = PixySnapper()
snapper.get_cropped_image(1, 1, 100, 100)
