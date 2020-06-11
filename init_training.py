#init training
#7.

exec(open("functions.py").read())

#os.environ["CUDA_VISIBLE_DEVICES"] = "" # for testing
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

x_train, y_train, x_test, y_test, labels = setup_load_cifar(verbose=True)
setup_tf(random_seed)

datagen = setup_data_aug()
# Compute quantities required for feature-wise normalization
# (std, mean, and principal components if ZCA whitening is applied).
datagen.fit(x_train)

exec(open("model.py").read())

#training