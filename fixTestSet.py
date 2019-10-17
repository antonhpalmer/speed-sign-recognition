#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

# import pandas as pd
# import csv
# import os
#
#
# imagesPath = 'GTSRB/Final_Test/Images/'
# inputCsvPath = 'GTSRB/Final_Training/Images/00007/GT-00008.csv'
# outputCsvPath = 'GT-00007.csv'
#
# classIds = [0, 1, 2, 3, 4, 5]
#
# with open(outputCsvPath, mode='w', newline='') as outputFile:
#     writer = csv.writer(outputFile, delimiter=';')
#     writer.writerow(['Filename', 'Width', 'Height', 'Roi.X1', 'Roi.Y1', 'Roi.X2', 'Roi.Y2', 'ClassId'])
#
#     test = pd.read_csv(inputCsvPath, sep=';')
#     for fileName, width, height, roiX1, roiY1, roiX2, roiY2, classId in zip(list(test['Filename']),
#                                                                             list(test['Width']), list(test['Height']),
#                                                                             list(test['Roi.X1']), list(test['Roi.Y1']),
#                                                                             list(test['Roi.X2']), list(test['Roi.Y2']),
#                                                                             list(test['ClassId'])):
#         writer.writerow([fileName, width, height, roiX1, roiY1, roiX2, roiY2, '7'])
#


