# Larger CNN for the MNIST Dataset
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K

from matplotlib import pyplot as plt

(X_train, y_train), (X_test, y_test) = cifar10.load_data()
# reshape to be [samples][width][height][pixels]
X_train = X_train.reshape(X_train.shape[0], 32, 32, 3).astype('float32')

plt.title('Label is {label}, Prediction is {pred}'.format(label=1, pred=123))
plt.imshow(X_test[1].reshape(32,32,3))
plt.show()

X_test = X_test.reshape(X_test.shape[0], 32, 32, 3).astype('float32')
# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255
# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

# define the larger model
def larger_model():
	# create model
	model = Sequential()
	model.add(Conv2D(30, (5, 5), input_shape=(32, 32, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Conv2D(15, (3, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.2))
	model.add(Flatten())
	model.add(Dense(128, activation='relu'))
	model.add(Dense(50, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

# build the model
model = larger_model()


# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

num = 15
prediction = model.predict(X_test[num].reshape(1,28,28,1))
label = y_test[num]
prediction = np.argmax(prediction, axis=1)

# print X_test[num].shape
plt.title('Label is {label}, Prediction is {pred}'.format(label=label, pred=prediction))
plt.imshow(X_test[num].reshape(28,28), cmap='gray')
plt.show()