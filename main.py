import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import numpy as np
import os
from matplotlib.pyplot import specgram


def main():

    base_dir = "/home/anthony/git/music_classification_lstm_rnn"
    #au_dir = base_dir + "/genres"
    #wav_dir = base_dir + "/wavfiles"
    #png_dir = base_dir + "/pngfiles"
    au_dir = base_dir + "/validation"
    wav_dir = base_dir + "/validation_wavfiles"
    png_dir = base_dir + "/validation_pngfiles"

    # Get all the base file names
    music_file_names = gen_music_file_names(au_dir)

    # Converting all our .au files to .wav files
    wav_file_names = convert_to_wav(music_file_names, wav_dir)

    # Take all the wav files and make them into pictures.
    # NOTE: Use this if you don't want to regenerate the wav files.
    #for wav_file in os.listdir(wav_file_dir):
    for wav_file in wav_file_names:
        make_spectrogram(os.path.join(wav_dir, wav_file), png_dir)


# convert_to_wav()
# Converts a given list of music filename's into wav files.
def convert_to_wav(music_file_names, wav_dir):
    wav_file_names = []
    for music_file_name in music_file_names:
        music_file_as_wav = ("".join(music_file_name.split(".")[0:2]) + ".wav").split("/")[-1]
        output_file_name = os.path.join(wav_dir, music_file_as_wav)
        os.system("sox -e signed-integer " + music_file_name + " " + output_file_name)
        wav_file_names.append(output_file_name)
    return wav_file_names


# make_spectrogram()
# Makes a given music file (.wav) into a spectrogram and saves it as a png.
def make_spectrogram(file_name, png_dir):

    sample_rate, samples = wavfile.read(file_name)
    figure = specgram(samples, Fs=sample_rate, xextent=(0,30))
    frame1 = plt.gca()
    fig = plt.gcf()
    # NOTE: This is inspired from original size of 483x356 images. 483 / 200 = 2.415
    fig.set_size_inches(2.415, 1.78)

    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    base_name = (os.path.basename(file_name))[:-4]

    # Saving the figure while removing white space border
    # NOTE: If you want smaller pictures, reduce the dpi.
    plt.savefig(os.path.join(png_dir, base_name + ".png"), bbox_inches='tight',
                pad_inches=-0.1, dpi=100)


# gen_music_file_names()
# Generating the full list of all music files in our code repo. Takes .au files
# and puts them into a list of absolute file paths.
def gen_music_file_names(au_dir, single_file = ""):
    music_file_names = []
    list_of_files = []
    for file_or_dir in os.listdir(au_dir):
        pre_path = os.path.join(au_dir, file_or_dir)
        if os.path.isdir(pre_path):
            for file in os.listdir(pre_path):
                list_of_files.append(os.path.join(full_path, file))
        elif os.path.isfile(pre_path):
            list_of_files.append(pre_path)

    # Figuring out which files we should be returning
    for file in list_of_files:
        # If single_file is specified (i.e. "blues.00000"),
        # then this will only process that file.
        if file.endswith(".au") and single_file in file:
            music_file_names.append(file)

    return music_file_names


if __name__ == "__main__":
    main()
