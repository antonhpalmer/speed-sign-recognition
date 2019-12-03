import validation.validator as validator
from PIL import Image
import os
import validation.circle_detection.CircleDetection as cd
import csv

dest_path = 'circle_detection/optimization_results/second/'
true_pos_path = 'C:/Users/sujee/PycharmProjects/speed-sign-recognition/validation/img/optimization/test/true/'
false_pos_path = 'C:/Users/sujee/PycharmProjects/speed-sign-recognition/validation/img/optimization/test/false/'

with open(dest_path + 'test.csv', 'w', newline='') as write_file:
    writer = csv.writer(write_file, delimiter=';')
    writer.writerow(['param1', '#Validated (from true)', '#Rejected (from true)', '#Validated (from false)',
                     '#Rejected (from false)', 'ErrorValue', 'ValidatedCorrectPercentage', 'RejectedCorrectPercentage' ])

    for param1 in range(200, 209):
        print("Status : " + str(param1) + " / 210")
        validated_from_true = 0
        rejected_from_true = 0
        validated_from_false = 0
        rejected_from_false = 0

        for root, subdirs, files in os.walk(true_pos_path):
            for file in files:
                filepath = os.path.join(root, file)
                image = Image.open(filepath)
                validated_image = cd.ValidatedImage(image)
                validated_image.circle_detection_with_params(20, param1, 26, 8, 0)
                if validated_image.is_valid:
                    validated_from_true += 1
                else:
                    rejected_from_true += 1

        for root, subdirs, files in os.walk(false_pos_path):
            # os.chdir(false_pos_path)
            for file in files:
                filepath = os.path.join(root, file)
                image = Image.open(filepath)
                validated_image = cd.ValidatedImage(image)
                validated_image.circle_detection_with_params(20, param1, 26, 8, 0)
                if validated_image.is_valid:
                    validated_from_false += 1
                else:
                    rejected_from_false += 1

        error_value = rejected_from_true + validated_from_false
        validated_correct_percentage = (100 * validated_from_true) / (validated_from_true + rejected_from_true)
        rejected_correct_percentage = (100 * rejected_from_false) / (rejected_from_false + validated_from_false)
        print(validated_correct_percentage)
        print(rejected_correct_percentage)
        writer.writerow([param1, validated_from_true, rejected_from_true, validated_from_false, rejected_from_false,
                         error_value, validated_correct_percentage, rejected_correct_percentage])
print("DONE")

