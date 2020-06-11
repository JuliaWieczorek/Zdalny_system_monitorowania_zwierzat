from keras.models import load_model
exec(open("functions.py").read())

num_predictions = 36

model = load_model('convnet_cifar10.kerasave')
x_train, y_train, x_test, y_test, labels = setup_load_cifar()
datagen = setup_data_aug()
datagen.fit(x_train)


predict_gen = model.predict_generator(datagen.flow(x_test, y_test,
    batch_size=batch_size, shuffle=False),
    steps=(x_test.shape[0] // batch_size)+1, workers=4)

indices = [np.random.choice(range(len(x_test)))
           for i in range(num_predictions)]

print(cifar_grid(x_test,y_test,indices,6,labels,predictions=predict_gen))

#zdjęcia