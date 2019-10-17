from PIL import Image

from boxfinder import return_coordinates

(x, y, z, w) = return_coordinates ('C:/Users/frede/OneDrive/Skrivebord/circle.jpg', (16, 16))
print (x, y, z, w)
