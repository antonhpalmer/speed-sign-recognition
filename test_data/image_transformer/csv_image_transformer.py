import csv
from path_transformer.output_path_creator import create_output_path


def transform_all_images_in_csv_file(csv_input_file_path):
    with open(csv_input_file_path, mode='r+') as input_file:
        csv_reader = csv.reader(input_file, delimiter= ';')
        output_csv_path = create_output_path(csv_input_file_path, ".csv", "(transformed)")
        with open(output_csv_path, mode='w', newline='') as outputFile:
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    # We just skip the first line containing the column names
                    line_count += 1
                else:
                    print(f'{row[0]} is a sign of type {row[1]}.')
                    line_count += 1
            print('We read a total of:', line_count, "lines")
            print(output_csv_path)


transform_all_images_in_csv_file('testdata_file.csv')