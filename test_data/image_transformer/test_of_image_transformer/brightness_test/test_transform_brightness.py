from test_data.image_transformer.brigthness_transformer import transform_brightness

output_path_list = transform_brightness("test.ppm", "test_image/")

assert (output_path_list[0] == "test_image/test(b=0.3).ppm")
assert (output_path_list[1] == "test_image/test(b=0.5).ppm")
assert (output_path_list[2] == "test_image/test(b=1.0).ppm")
assert (output_path_list[3] == "test_image/test(b=1.5).ppm")
assert (output_path_list[4] == "test_image/test(b=2.0).ppm")
assert (output_path_list[5] == "test_image/test(b=2.3).ppm")