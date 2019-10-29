import csv
from path_transformer.output_path_creator import create_output_path


def transform_all_images_in_csv_file(csv_input_file_path):
    with open(csv_input_file_path, mode='r+') as input_file:
        output_csv_path = create_output_path(csv_input_file_path, ".csv", "(transformed)")
        with open(output_csv_path, mode='w', newline='') as outputFile:
            print(output_csv_path)


transform_all_images_in_csv_file('trainingdata_file.csv')