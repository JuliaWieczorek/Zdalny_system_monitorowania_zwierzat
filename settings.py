#1.
#settings.py

import os

def path_to_images():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    path_dirname = script_dir.replace('\\', '/')
    rel_path = "images"
    path = os.path.join(path_dirname, rel_path)
    path = path.replace('\\', '/')
    return path

x = path_to_images()

def create_classification_dirs():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    path_dirname = script_dir.replace('\\', '/')
    rel_path = "images/final"
    path = os.path.join(path_dirname, rel_path)
    path = path.replace('\\', '/')
    if not os.path.isdir(path):
        os.makedirs(os.path.join(path))
    cats = "images/final/cats"
    cats = os.path.join(path_dirname, cats)
    cats = cats.replace('\\', '/')
    if not os.path.isdir(cats):
        os.makedirs(os.path.join(cats))
    dogs = "images/final/dogs"
    dogs = os.path.join(path_dirname, dogs)
    dogs = dogs.replace('\\', '/')
    if not os.path.isdir(dogs):
        os.makedirs(os.path.join(dogs))
    return path

create_classification_dirs()
script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
path_dirname = script_dir.replace('\\', '/')
path_train = "images/final/cats"
f = os.path.join(path_dirname, path_train)
