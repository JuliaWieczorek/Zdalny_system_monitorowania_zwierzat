#1.
#settings.py

import os
"""
batch_size = 128
num_classes = 10
epochs_shortrun = 5
epochs_longrun = 500
random_seed = 343
"""
def path_to_images():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    path_dirname = script_dir.replace('\\', '/')
    rel_path = "classification_images/cats_and_dogs_filtered"
    path = os.path.join(path_dirname, rel_path)
    path = path.replace('\\', '/')
    return path

def path_to_chicken():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    path_dirname = script_dir.replace('\\', '/')
    rel_path = "classification_images/chicken"
    path = os.path.join(path_dirname, rel_path)
    filePath = path.replace('\\', '/')
    return filePath

x = path_to_images()
save_dir = x + 'work'
res_dir = x + 'results'
model_name = x + 'model'

# setup paths
import os

ckpt_dir = os.path.join(save_dir,"checkpoints")
if not os.path.isdir(ckpt_dir):
    os.makedirs(ckpt_dir)

### moje
if not os.path.isdir(res_dir):
    os.makedirs(os.path.join(res_dir))

if not os.path.isdir(model_name):
    os.makedirs(os.path.join(model_name))

model_path = os.path.join(res_dir, model_name + ".kerasave")
hist_path = os.path.join(res_dir, model_name + ".kerashist")