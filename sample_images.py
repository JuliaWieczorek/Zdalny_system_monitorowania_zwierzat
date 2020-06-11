#4.
import matplotlib
exec(open("functions.py").read())

x_train, y_train, x_test, y_test, labels = setup_load_cifar(verbose=True)

indices = [np.random.choice(range(len(x_train))) for i in range(36)]

cifar_grid(x_train,y_train,indices,6,labels)
#x_train shape: (50000, 32, 32, 3), 50000 train samples, 10000 test samples.
#sample images