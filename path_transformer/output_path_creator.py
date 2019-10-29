import re
from path_transformer.path_exception import PathException


def create_output_path(path_to_input_file, file_type, appended_name):
    info = re.search('(.+?)' + file_type, path_to_input_file)
    if info:
        return str(info.group(1) + appended_name + file_type)
    else:
        raise PathException('The given path:', path_to_input_file, ", did not end on: ", file_type)