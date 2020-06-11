exec(open("functions.py").read())

import keras
import tensorflow as tf
import numpy as np
import FetchMail as fm

sess = tf.compat.v1.Session()

model = keras.models.load_model('model.kerasave')
exec(open("functions.py").read())

_,_,_,_,labels = setup_load_cifar()
img = tf.io.read_file(fm.FetchEmail.filePath)
# img = tf.io.read_file('C:/Users/julia/Documents/bioinformatyka/classification_images/cats_and_dogs_filtered/cat.1.jpg')
img = tf.image.decode_jpeg(img, channels=3)
img.set_shape([None, None, 3])
img = tf.image.resize(img, (32, 32))
from keras.preprocessing import image
img = image.img_to_array(img) # convert to numpy array
img = np.expand_dims(img, 0) # make 'batch' of 1

pred = model.predict(img)
pred = labels["label_names"][np.argmax(pred)]
print(pred)

#tak to ma działać o wstateczności