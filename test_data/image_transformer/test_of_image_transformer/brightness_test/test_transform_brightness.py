from test_data.image_transformer.brigthness_transformer import transform_brightness

output_path_list = transform_brightness("test.ppm", "test_image/")

assert (output_path_list[0] == "test(b=0.3).ppm")
assert (output_path_list[1] == "test(b=0.5).ppm")
assert (output_path_list[2] == "test(b=1.0).ppm")
assert (output_path_list[3] == "test(b=1.5).ppm")
assert (output_path_list[4] == "test(b=2.0).ppm")
assert (output_path_list[5] == "test(b=2.3).ppm")