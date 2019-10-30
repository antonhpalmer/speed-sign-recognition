import csv
import re
from path_transformer.output_path_creator import create_output_path
from test_data.image_transformer.brigthness_transformer import transform_brightness
from path_transformer.path_exception import PathException


def transform_all_images_in_csv_file(csv_input_file_path, image_folder_path):
    with open(csv_input_file_path, mode='r+') as input_file:
        csv_input_reader = csv.reader(input_file, delimiter= ';')

        output_csv_path = create_output_path(csv_input_file_path, ".csv", "(transformed)")
        with open(output_csv_path, mode='w', newline='') as outputFile:
            csv_output_writer = csv.writer(outputFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            line_count = 0
            for row in csv_input_reader:
                if line_count == 0:
                    # We just write the first line containing the column names
                    csv_output_writer.writerow(row)
                    line_count += 1
                else:
                    output_image_names = transform_brightness(row[0], image_folder_path)
                    # We here write all the new images to the csv file
                    for output_name in output_image_names:
                        csv_output_writer.writerow([output_name, row[1]])
                    line_count += 1
