# #  Copyright (c) 2019.
# #  AAU, Student project group sw504e19, 2019.
# #  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import pandas as pd
import csv
import os

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


# training_images_path = 'test_data/training_images/transformed/'
# training_output_path = 'test_data/training_images/'
# test_images_path = 'test_data/test_images/'
# input_csv_path = 'test_data/new_training_data.csv'
# test_output_csv_path = 'test_data/test_file.csv'
#
#
# with open(test_output_csv_path, mode='w', newline='') as output_csv_file:
#     writer = csv.writer(output_csv_file, delimiter=';')
#     writer.writerow(['Filename', 'ClassId'])
#
#     test = pd.read_csv(input_csv_path, sep=';')
#     pic_count = 0
#     for filename, classId in zip(list(test['Filename']), list(test['ClassId'])):
#         file_path = training_images_path + filename
#         if not os.path.exists(file_path):
#             continue
#         pic_count += 1
#         print('Pic ' + str(pic_count))
#         if pic_count % 5 == 0:
#             # every 5th pic, make it a test pic
#             os.makedirs(test_images_path, exist_ok=True)
#             os.replace(file_path, test_images_path + filename)
#             writer.writerow([filename, classId])
#
#         else:
#             os.makedirs(training_output_path + str(classId) + '/', exist_ok=True)
#             os.replace(file_path, training_output_path + str(classId) + '/' + filename)
#
#
#

