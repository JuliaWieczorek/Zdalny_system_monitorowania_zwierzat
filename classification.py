import numpy as np
import pandas as pd
from keras.preprocessing.image import ImageDataGenerator, load_img
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.utils import plot_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import random
import os
from settings import path_to_images, ckpt_dir
import tensorflow as tf
import keras


# define constants
FAST_RUN = False
IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_CHANNELS = 3

def prepare_data():
    """PREPARE TRAINING DATA"""
    path = path_to_images()
    path = os.path.join(path, "train")
    path = path.replace('\\', '/')
    filenames = os.listdir(path)

    categories = []
    for filename in filenames:
        category = filename.split('.')[0]
        if category == 'dog':
            categories.append(1)
        else:
            categories.append(0)

    return (filenames, path, categories)

def plot():
    x = prepare_data()
    df = pd.DataFrame({'filename': x[0], 'category': x[2]})
    df['category'].value_counts().plot.bar()
    plt.show()

def random_image():
    """SHOW RANDOM IMAGE"""
    data = prepare_data()
    sample = random.choice(data[0])
    image = load_img(data[1] + '/' + sample)
    plt.imshow(image)
    plt.show()

def create_model():
    """MODEL
    zapisuje plik do work/checkpoints/weights-improvement-{epoch:02d}.hdf5
    oraz model do results/model.svg"""

    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Activation, BatchNormalization

    model = Sequential()

    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))  # 2 because we have cat and dog classes

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    model.summary()

    exec(open("settings.py").read())
    filepath = os.path.join(ckpt_dir, "weights-improvement-{epoch:02d}.hdf5")
    checkpoint = ModelCheckpoint(filepath, monitor="val_acc", verbose=1, save_best_only=True, mode="max")
    print("Saving improvement checkpoints to \n\t{0}".format(filepath))
    return model

def model_analysis():
    import os
    from keras.utils import plot_model
    model = create_model()
    path_dirname = os.path.abspath(__file__)
    path_dirname = os.path.split(path_dirname)[0]
    path_dirname = path_dirname.replace('\\', '/')
    rel_path = "results/model.svg"
    path = os.path.join(path_dirname, rel_path)
    path = path.replace('\\', '/')

    plot_model(model, to_file=path, show_layer_names=True, show_shapes=True, rankdir="TB")
    print(model.summary())

# model_analysis()

def training():
    """TRAINING
    barplot with dogs and cats"""
    from keras.callbacks import EarlyStopping, ReduceLROnPlateau

    # early stop callback, given a bit more leeway

    earlystop = EarlyStopping(patience=10)

    learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc', patience=2, verbose=1, factor=0.5, min_lr=0.00001)
    callbacks = [earlystop, learning_rate_reduction]

    # prepare date
    x = prepare_data()
    df = pd.DataFrame({'filename': x[0], 'category': x[2]})
    df["category"] = df["category"].replace({0: 'cat', 1: 'dog'})

    train_df, validate_df = train_test_split(df, test_size=0.20, random_state=42)
    train_df = train_df.reset_index(drop=True)
    validate_df = validate_df.reset_index(drop=True)

    train_df['category'].value_counts().plot.bar()
    plt.show()

    validate_df['category'].value_counts().plot.bar()

    total_train = train_df.shape[0]
    total_validate = validate_df.shape[0]
    batch_size = 15

    # training_generator
    train_datagen = ImageDataGenerator(rotation_range=15, rescale=1. / 255, shear_range=0.1, zoom_range=0.2,
                                       horizontal_flip=True, width_shift_range=0.1, height_shift_range=0.1)
    train_generator = train_datagen.flow_from_dataframe(train_df, prepare_data()[1], x_col='filename', y_col='category',
                                                        target_size=IMAGE_SIZE, class_mode='categorical',
                                                        batch_size=batch_size)
    # output: Found 1599 validated image filenames belonging to 2 classes.

    # validation_generator():
    validation_datagen = ImageDataGenerator(rescale=1. / 255)
    validation_generator = validation_datagen.flow_from_dataframe(validate_df, prepare_data()[1], x_col='filename', y_col='category',
                                                                  target_size=IMAGE_SIZE, class_mode='categorical',
                                                                  batch_size=batch_size)

    #output: Found 401 validated image filenames belonging to 2 classes.
    return(train_df, train_datagen, train_generator, validation_generator, total_validate, batch_size, total_train,
           callbacks)

def example_work():
    """HOW WORK"""
    x = training()
    example_df = x[0].sample(n=1).reset_index(drop=True)
    example_generator = x[1].flow_from_dataframe(example_df, prepare_data()[1], x_col='filename', y_col='category',
                                                          target_size=IMAGE_SIZE, class_mode='categorical')

    # plot
    plt.figure(figsize=(12, 12))
    for i in range(0, 15):
        plt.subplot(5, 3, i + 1)
        for X_batch, Y_batch in example_generator:
            image = X_batch[0]
            plt.imshow(image)
            break
    plt.tight_layout()
    plt.show()
    # jedno zdjęcie przy różnych kątach

def fit_model():
    x = training()
    epochs = 3 if FAST_RUN else 50
    model = create_model()
    history = model.fit_generator(x[2], epochs=epochs, validation_data=x[3], validation_steps=x[4] // x[5],
                                  steps_per_epoch=x[6] // x[5], callbacks=x[7])
    model.save_weights("model.h5")

    filepath = os.path.join(ckpt_dir, "weights-improvement-{epoch:02d}-{val_acc:.6f}.hdf5")
    checkpoint = ModelCheckpoint(filepath, monitor="val_acc", verbose=1, save_best_only=True, mode="max")
    print("Saving improvement checkpoints to \n\t{0}".format(filepath))
    # early stop callback, given a bit more leeway
    stahp = EarlyStopping(min_delta=0.00001, patience=25)

    from settings import path_to_images
    y = path_to_images()
    res_dir = y + 'results'
    if not os.path.isdir(res_dir):
        os.makedirs(os.path.join(res_dir))
    model_path = os.path.join(res_dir, "model.kerasave")
    model.save(model_path)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    ax1.plot(history.history['loss'], color='b', label="Training loss")
    ax1.plot(history.history['val_loss'], color='r', label="validation loss")
    ax1.set_xticks(np.arange(1, epochs, 1))
    ax1.set_yticks(np.arange(0, 1, 0.1))

    ax2.plot(history.history['accuracy'], color='b', label="Training accuracy")
    ax2.plot(history.history['val_accuracy'], color='r', label="Validation accuracy")
    ax2.set_xticks(np.arange(1, epochs, 1))

    legend = plt.legend(loc='best', shadow=True)
    plt.tight_layout()
    plt.show()

def load_session():
    """LOAD LAST SESSION"""
    sess = tf.compat.v1.Session()
    # model = keras.models.load_model('model.h5')
    filepath = os.path.join("classification_images/cats_and_dogs_filteredresults/model.kerasave")
    model = keras.models.load_model(filepath)
    model.load_weights(filepath)

def create_test_generator():
    """PREPARE TESTING DATA"""
    path = path_to_images()
    path = os.path.join(path, "validation")
    path = path.replace('\\', '/')
    test_filenames = os.listdir(path)
    test_df = pd.DataFrame({'filename': test_filenames})
    nb_samples = test_df.shape[0]

    """CREATE TESTING GENERATOR"""
    batch_size = 15
    test_gen = ImageDataGenerator(rescale=1. / 255)
    test_generator = test_gen.flow_from_dataframe(test_df, path, x_col='filename', y_col=None, class_mode=None,
                                                  target_size=IMAGE_SIZE, batch_size=batch_size, shuffle=False)

def predict():
    sess = tf.compat.v1.Session()
    # model = keras.models.load_model('model.h5')
    filepath = os.path.join("classification_images/cats_and_dogs_filteredresults/model.kerasave")
    model = keras.models.load_model(filepath)
    model.load_weights(filepath)

    """PREPARE TESTING DATA"""
    path = path_to_images()
    path = os.path.join(path, "validation")
    path = path.replace('\\', '/')
    test_filenames = os.listdir(path)
    test_df = pd.DataFrame({'filename': test_filenames})
    nb_samples = test_df.shape[0]

    """CREATE TESTING GENERATOR"""
    batch_size = 15
    test_gen = ImageDataGenerator(rescale=1. / 255)
    test_generator = test_gen.flow_from_dataframe(test_df, path, x_col='filename', y_col=None, class_mode=None,
                                                  target_size=IMAGE_SIZE, batch_size=batch_size, shuffle=False)


    predict = model.predict_generator(test_generator, steps=np.ceil(nb_samples / batch_size))

    test_df['category'] = np.argmax(predict, axis=-1)

    label_map = dict((v, k) for k, v in train_generator.class_indices.items())
    test_df['category'] = test_df['category'].replace(label_map)

    test_df['category'] = test_df['category'].replace({'dog': 1, 'cat': 0})

    test_df['category'].value_counts().plot.bar()

    sample_test = test_df.head(18)
    sample_test.head()
    plt.figure(figsize=(12, 24))
    for index, row in sample_test.iterrows():
        filename = row['filename']
        category = row['category']
        img = load_img(path + '/' + filename, target_size=IMAGE_SIZE)
        plt.subplot(6, 3, index + 1)
        plt.imshow(img)
        plt.xlabel(filename + '(' + "{}".format(category) + ')')
    plt.tight_layout()
    plt.show()

def submission():
    submission_df = test_df.copy()
    submission_df['id'] = submission_df['filename'].str.split('.').str[0]
    submission_df['label'] = submission_df['category']
    submission_df.drop(['filename', 'category'], axis=1, inplace=True)
    submission_df.to_csv('submission.csv', index=False)

predict()