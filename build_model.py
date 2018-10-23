
from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Sequential
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.optimizers import SGD

import numpy as np


X_train = np.load("X_train.dat")
y_train = np.load("y_train.dat")

X_train = X_train/255
print(X_train)

print(X_train.shape)
print(y_train.shape)

model = Sequential()
# input: 100x100 images with 3 channels -> (100, 100, 3) tensors.
# this applies 32 convolution filters of size 3x3 each.
model.add(Conv2D(32, (7, 7), activation='relu', input_shape=X_train.shape[1:]))
model.add(Conv2D(32, (7, 7), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
# model.add(Dropout(0.9))
model.add(Dense(10, activation='softmax'))

# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

model.compile('adam', 'categorical_crossentropy',metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=32, epochs=10)

score = model.evaluate(X_train, y_train, batch_size=32, verbose=1)

# X_input = Input(X_train[1:].shape)
#
# # Zero-Padding: pads the border of X_input with zeroes
# # X = ZeroPadding2D((3, 3))(X_input)
#
# # CONV -> BN -> RELU Block applied to X
# X = X_input
# X = Conv2D(32, (7, 7), strides=(1, 1), name='conv0')(X)
# X = BatchNormalization(axis=3, name='bn0')(X)
# X = Activation('relu')(X)
#
# # MAXPOOL
# X = MaxPooling2D((2, 2), name='max_pool')(X)
#
# # FLATTEN X (means convert it to a vector) + FULLYCONNECTED
# X = Flatten()(X)
# X = Dense(10, activation='softmax', name='fc')(X)
#
# # Create model. This creates your Keras model instance, you'll use this instance to train/test the model.
# model = Model(inputs=X_input, outputs=X, name='HappyModel')
