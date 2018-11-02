import numpy as np
from skimage.io import imread
import os

def main():
    convert_training_images()
    convert_validation_images()

def convert_training_images():
    X_train = []
    y_train = []
    label = []
    current_wd = os.getcwd()
    for file in os.listdir(current_wd + "/split_pngfiles"):
        print(file)
        image = imread(current_wd + "/split_pngfiles/" + file)
        image = image[:, :, 0]
        # image = image.reshape([124, 174, 3])
        X_train.append(image)

        if "blues" in file:
            label = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif "classical" in file:
            label = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        elif "country" in file:
            label = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        elif "disco" in file:
            label = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        elif "hiphop" in file:
            label = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        elif "jazz" in file:
            label = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        elif "metal" in file:
            label = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        elif "pop" in file:
            label = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        elif "reggae" in file:
            label = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        elif "rock" in file:
            label = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

        y_train.append(label)

    print(np.array(X_train).shape)
    print(np.array(y_train).shape)
    np.array(X_train).dump("X_train.dat")
    np.array(y_train).dump("y_train.dat")

def convert_validation_images():
    X_test = []
    current_wd = os.getcwd()
    for file in os.listdir(current_wd + "/validation_split_pngfiles"):
        print(file)
        image = imread(current_wd + "/validation_split_pngfiles/" + file)
        image = image[:, :, 0]
        # image = image.reshape([124, 174, 3])
        X_test.append(image)

    print(np.array(X_test).shape)
    np.array(X_test).dump("X_test.dat")

if __name__ == "__main__":
    main()
