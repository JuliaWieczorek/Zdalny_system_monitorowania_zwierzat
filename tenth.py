exec(open("functions.py").read())

from keras.models import load_model

x_train, y_train, x_test, y_test, labels = setup_load_cifar()
datagen = setup_data_aug()
datagen.fit(x_train)

model = load_model('convnet_cifar10.kerasave')

# Evaluate model with test data set
evaluation = model.evaluate_generator(datagen.flow(x_test, y_test,
    batch_size=batch_size, shuffle=False),
    steps=x_test.shape[0] // batch_size, workers=4)

# Print out final values of all metrics
key2name = {'accuracy':'Accuracy', 'loss':'Loss', 'val_acc':'Validation Accuracy', 'val_loss':'Validation Loss'}
#key2name = {'acc':'Accuracy', 'loss':'Loss', 'val_acc':'Validation Accuracy', 'val_loss':'Validation Loss'}
#print(model.metrics_names)
results = []
for i,key in enumerate(model.metrics_names):
    results.append('%s = %.2f' % (key2name[key], evaluation[i]))
print(", ".join(results))
#loss, accuracy