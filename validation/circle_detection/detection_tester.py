import cv2
import os
import numpy as np
from validation.circle_detection.CircleDetectionSkabelon import circle_detection

# Read image.
validated_counter = 0
rejected_counter = 0

for i in range(0, 700):

    #src_path = '../testdata/Images/' + str(i) + '.ppm'
    src_path = 'C:/Users/sujee/Desktop/P5/Images/' + str(i) + '.ppm'
    if os.path.exists(src_path):
        #dest_path = '/test_detection/'
        dest_path = 'C:/Users/sujee/PycharmProjects/speed-sign-recognition/validation/test_detection/'
        dest_name = 'test' + str(i) + '.jpg'
        img = cv2.imread(src_path, cv2.IMREAD_COLOR)
        if circle_detection(img, dest_path, dest_name, i):
            validated_counter += 1
        else:
            rejected_counter +=1

print('Validated images: ' + str(validated_counter))
print('Rejected images: ' + str(rejected_counter))


