import Augmentor
import os
path = "G:/22.08.17code/monitor/data/images"
file_names = os.listdir(path)

for name in file_names:
    img = Augmentor.Pipeline(name)
    img.flip_left_right(probability=1.0)
    img.rotate_without_crop(probability=1, max_left_rotation=0.8, max_right_rotation=0.8, expand=False, fillcolor=None)

    img.sample(4970)
