from PIL import Image
import os
import csv
from validation.dim_validator import valid_dimensions
import validation.circle_detection.CircleDetection as cd



counter = 0
dest_path = 'circle_detection/optimization_results/second/'
true_pos_path = os.path.abspath('img/optimization/training/true/')
false_pos_path = os.path.abspath('img/optimization/training/false/')

with open(dest_path + 'minDistance.csv', 'w', newline='') as write_file:
    writer = csv.writer(write_file, delimiter=';')
    writer.writerow(['minDistance', '#Validated (from true)', '#Rejected (from true)', '#Validated (from false)',
                     '#Rejected (from false)', 'ErrorValue'])

    for minDistance in range (1, 204):
        validated_from_true = 0
        rejected_from_true = 0
        validated_from_false = 0
        rejected_from_false = 0
        print("Status: " + str(minDistance) + ' / 204')

        for root, subdirs, files in os.walk(true_pos_path):
            #os.chdir(true_pos_path)
            for file in files:
                filepath = os.path.join(root, file)
                image = Image.open(filepath)
                validated_image = cd.ValidatedImage(image)
                validated_image.circle_detection_with_params(minDistance, 50, 30, 10, 0)
                if validated_image.is_valid:
                    validated_from_true += 1
                else:
                    rejected_from_true += 1

        for root, subdirs, files in os.walk(false_pos_path):
            #os.chdir(false_pos_path)
            for file in files:
                filepath = os.path.join(root, file)
                image = Image.open(filepath)
                validated_image = cd.ValidatedImage(image)
                validated_image.circle_detection_with_params(minDistance, 50, 30, 10, 0)
                if validated_image.is_valid:
                    validated_from_false += 1
                else:
                    rejected_from_false += 1
        error_value = rejected_from_true + validated_from_false
        writer.writerow([minDistance, validated_from_true, rejected_from_true, validated_from_false, rejected_from_false, error_value ])
    print("DONE")








