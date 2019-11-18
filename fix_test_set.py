# #  Copyright (c) 2019.
# #  AAU, Student project group sw504e19, 2019.
# #  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import pandas as pd
import csv
import os
from classification.definitions import SIGN_TO_ID_SWITCHER

# classIds = [0, 1, 2, 3, 4, 5]

# import os
# import csv
# import pandas as pd
# image_dir_path = 'path/to/image/'
# input_csv_path = 'path/to/csv.csv'
# output_csv_path = 'path/to/new_csv.csv'
#
# with open(output_csv_path, mode='w', newline='') as output_file:
#     writer = csv.writer(output_file, delimiter=';')
#     writer.writerow(['Filename', 'ClassId'])
#
#     input_file = pd.read_csv(input_csv_path, sep=';')
#     for filename, class_id in zip(list(input_file['Filename']), list(input_file['ClassId'])):
#         if os.path.exists(image_dir_path + filename):
#             writer.writerow([filename, class_id])


# training_images_path = 'test_data/training_images/'
# training_output_path = 'test_data/training_images/'
# test_images_path = 'test_data/test_images/'
# input_csv_path = 'test_data/test_file.csv'
# test_output_csv_path = 'test_data/test_file_new.csv'
#
#
# with open(test_output_csv_path, mode='w', newline='') as output_csv_file:
#     writer = csv.writer(output_csv_file, delimiter=';')
#     writer.writerow(['Filename', 'ClassId'])
#
#     test = pd.read_csv(input_csv_path, sep=';')
#     pic_count = 0
#     for filename, class_id in zip(list(test['Filename']), list(test['ClassId'])):
#         writer.writerow([filename, SIGN_TO_ID_SWITCHER.get(class_id)])


input_images_path = 'test_data/new_test_images/'
output_path = 'test_data/new_test_images_separated/'
# test_images_path = 'test_data/test_images/'
input_csv_path = 'test_data/new_testdata_file.csv'
# test_output_csv_path = 'test_data/test_file.csv'


test = pd.read_csv(input_csv_path, sep=';')
for filename, class_id in zip(list(test['Filename']), list(test['ClassId'])):
    if os.path.exists(input_images_path + filename):
        output_dir = output_path + str(class_id) + '/'
        os.makedirs(output_dir, exist_ok=True)
        os.replace(input_images_path + filename,
                   output_dir + filename)



