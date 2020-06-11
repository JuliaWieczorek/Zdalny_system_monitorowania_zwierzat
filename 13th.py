import keras
import tensorflow as tf
import numpy as np

sess = tf.compat.v1.Session()

#sess = keras.backend.get_session()
exec(open("functions.py").read())
model = keras.models.load_model('convnet_cifar10.kerasave')
_,_,_,_,labels = setup_load_cifar()

img = tf.read_file('Qat.jpg')
img = tf.image.decode_jpeg(img, channels=3)
img.set_shape([None, None, 3])
img = tf.image.resize_images(img, (32, 32))
img = img.eval(session=sess) # convert to numpy array
img = np.expand_dims(img, 0) # make 'batch' of 1

pred = model.predict(img)
pred = labels["label_names"][np.argmax(pred)]
pred

#'cat'