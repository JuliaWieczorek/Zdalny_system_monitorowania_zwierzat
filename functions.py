#functions.py
#2.

exec(open("settings.py").read())

import numpy as np
import dill as pickle
from math import *


def setup_tf(seed):
    import os
    import random
    import numpy as np
    import tensorflow as tf
    from tensorflow.python.framework import ops
    ops.reset_default_graph()
    #tf.reset_default_graph()
    # set random seeds for reproducibility
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    #tf.set_random_seed(seed)
    #ops.set_random_seed(seed)



def setup_load_cifar(verbose=False):
    import os #shutil
    from keras.datasets import cifar10
    from keras.utils import to_categorical

    # The data, shuffled and split between train and test sets:
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    if verbose:
        print("x_train shape: {}, {} train samples, {} test samples.\n".format(
            x_train.shape, x_train.shape[0], x_test.shape[0]))

    # Convert class vectors to binary class matrices.
    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)

    x_train = x_train.astype("float32")
    x_test = x_test.astype("float32")
    x_train /= 255.0
    x_test /= 255.0

    # Load label names to use in prediction results
    label_list_path = "datasets/cifar-10-batches-py/batches.meta"

    keras_dir = os.path.expanduser(os.path.join("~", ".keras"))
    datadir_base = os.path.expanduser(keras_dir)
    if not os.access(datadir_base, os.W_OK):
        datadir_base = os.path.join("/tmp", ".keras")
    label_list_path = os.path.join(datadir_base, label_list_path)

    with open(label_list_path, mode="rb") as f:
        labels = pickle.load(f)

    return x_train, y_train, x_test, y_test, labels


def setup_data_aug():
    print("Using real-time data augmentation.\n")
    # This will do preprocessing and realtime data augmentation:
    from keras.preprocessing.image import ImageDataGenerator

    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=0,  # randomly rotate images in the range
        # (degrees, 0 to 180)
        width_shift_range=0.1,  # randomly shift images horizontally
        # (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically
        # (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False  # randomly flip images
    )

    return datagen


# Function to find latest checkpoint file
def last_ckpt(dir):
    fl = os.listdir(dir)
    fl = [x for x in fl if x.endswith(".hdf5")]
    cf = ""
    if len(fl) > 0:
        accs = [float(x.split("-")[3][0:-5]) for x in fl]
        m = max(accs)
        iaccs = [i for i, j in enumerate(accs) if j == m]
        fl = [fl[x] for x in iaccs]
        epochs = [int(x.split("-")[2]) for x in fl]
        cf = fl[epochs.index(max(epochs))]
        cf = os.path.join(dir, cf)

    return cf


# Visualizing CIFAR 10, takes indicides and shows in a grid
def cifar_grid(X, Y, inds, n_col, labels, predictions=None):
    import matplotlib.pyplot as plt
    if predictions is not None:
        if Y.shape != predictions.shape:
            print("Predictions must equal Y in length!\n")
            return (None)
    N = len(inds)
    n_row = int(ceil(1.0 * N / n_col))
    fig, axes = plt.subplots(n_row, n_col, figsize=(10, 10))

    clabels = labels["label_names"]
    for j in range(n_row):
        for k in range(n_col):
            i_inds = j * n_col + k
            i_data = inds[i_inds]

            axes[j][k].set_axis_off()
            if i_inds < N:
                axes[j][k].imshow(X[i_data, ...], interpolation="nearest")
                label = clabels[np.argmax(Y[i_data, ...])]
                axes[j][k].set_title(label)
                if predictions is not None:
                    pred = clabels[np.argmax(predictions[i_data, ...])]
                    if label != pred:
                        label += " n"
                        axes[j][k].set_title(pred, color="red")

        fig.set_tight_layout(True)
        return fig