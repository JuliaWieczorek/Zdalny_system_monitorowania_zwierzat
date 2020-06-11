#model.py
#5.

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D
from keras.optimizers import Adam
from keras.layers.pooling import MaxPooling2D
from keras.callbacks import ModelCheckpoint,EarlyStopping
###### from sample images
import matplotlib
exec(open("functions.py").read())

x_train, y_train, x_test, y_test, labels = setup_load_cifar(verbose=True)

indices = [np.random.choice(range(len(x_train))) for i in range(36)]
#######
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=x_train.shape[1:]))
model.add(Conv2D(64, kernel_size=(3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(10, activation="softmax"))


# initiate Adam optimizer
opt = Adam(lr=0.0001, decay=1e-6)

# Let's train the model using RMSprop
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# checkpoint callback
#filepath = os.path.join(ckpt_dir, "weights-improvement-{epoch:02d}-{val_acc:.6f}.hdf5")
filepath = os.path.join(ckpt_dir, "weights-improvement-{epoch:02d}.hdf5")
checkpoint = ModelCheckpoint(filepath, monitor="val_acc", verbose=1, save_best_only=True, mode="max")
print("Saving improvement checkpoints to \n\t{0}".format(filepath))
# early stop callback, given a bit more leeway
stahp = EarlyStopping(min_delta=0.00001, patience=25)