from test_data.image_transformer.csv_image_transformer import transform_all_images_in_csv_file
import os
import csv
import pandas as pd

image_dir_path = 'test_images/'
input_csv_path = 'test_file.csv'
trimmed_csv_path = 'trimmed_test_data.csv'

with open(trimmed_csv_path, mode='w', newline='') as output_file:
    writer = csv.writer(output_file, delimiter=';')
    writer.writerow(['Filename', 'ClassId'])

    input_file = pd.read_csv(input_csv_path, sep=';')
    for filename, class_id in zip(list(input_file['Filename']), list(input_file['ClassId'])):
        if os.path.exists(image_dir_path + filename):
            writer.writerow([filename, class_id])

transform_all_images_in_csv_file(trimmed_csv_path, image_dir_path)
