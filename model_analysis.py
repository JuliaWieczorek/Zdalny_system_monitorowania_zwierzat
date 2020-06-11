#6.
import os
exec(open("model.py").read())
from keras.utils import plot_model

path_dirname = os.path.abspath(__file__)
path_dirname = os.path.split(path_dirname)[0]
path_dirname = path_dirname.replace('\\', '/')
rel_path = "results/model.svg"
path = os.path.join(path_dirname, rel_path)
path = path.replace('\\', '/')
print(path)

plot_model(model, to_file=path, show_layer_names=True, show_shapes=True, rankdir="TB")
print(model.summary())

#wydruk modelu-> model ananlysis