from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Sequential
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.optimizers import SGD
from keras.models import load_model
import numpy as np
import os
from keras import backend as K
K.clear_session()

# Load in pre-trained model for music classification
model = load_model("trained_music_classifier.h5")

X_test = np.load("X_test.dat")
# normalize testing data
X_test = X_test / 255

# make predictions on validation data from Kaggle
predictions = model.predict_classes(X_test, verbose=1)
# Converting predictions to genre names
predictions

prediction_names = []
for prediction in predictions:
    if prediction == 0:
        prediction_names.append("blues")
    elif prediction == 1:
        prediction_names.append("classical")
    elif prediction == 2:
        prediction_names.append("country")
    elif prediction == 3:
        prediction_names.append("disco")
    elif prediction == 4:
        prediction_names.append("hiphop")
    elif prediction == 5:
        prediction_names.append("jazz")
    elif prediction == 6:
        prediction_names.append("metal")
    elif prediction == 7:
        prediction_names.append("pop")
    elif prediction == 8:
        prediction_names.append("reggae")
    else:
        prediction_names.append("rock")
prediction_names

list_of_file_names = []
for file in os.listdir(os.getcwd() + "/validation_pngfiles"):
    file = file.replace("png", "au")
    file = file.split("ion")
    file = file[0] + "ion" + "." + file[1]
    print(file)
    list_of_file_names.append(file)

output_file = open("output.csv", "w")
output_file.write("id,class\n")

i = 0
for prediction in prediction_names:
    output_file.write("%s,%s\n" % (list_of_file_names[i], prediction))
    i += 1

output_file.close()
