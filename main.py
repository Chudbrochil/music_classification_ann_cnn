import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import numpy as np
import os
from matplotlib.pyplot import specgram


def main():

    base_dir = "/home/anthony/git/music_classification_lstm_rnn"
    au_file_dir = base_dir + "/genres"
    wav_file_dir = base_dir + "/wavfiles"
    png_dir = base_dir + "/pngfiles"

    # Get all the base file names
    #music_file_names = gen_music_file_names(au_file_dir)

    # Converting all our .au files to .wav files
    #wav_file_names = convert_to_wav(music_file_names, wav_file_dir)

    # Take all the wav files and make them into pictures.
    for wav_file in os.listdir(wav_file_dir):
        make_spectrogram(os.path.join(wav_file_dir, wav_file), png_dir)


# convert_to_wav()
# Converts a given list of music filename's into wav files.
def convert_to_wav(music_file_names, wav_file_dir):
    wav_file_names = []
    for music_file_name in music_file_names:
        music_file_as_wav = ("".join(music_file_name.split(".")[0:2]) + ".wav").split("/")[-1]
        output_file_name = os.path.join(wav_file_dir, music_file_as_wav)
        os.system("sox -e signed-integer " + music_file_name + " " + output_file_name)
        wav_file_names.append(output_file_name)
    return wav_file_names


# make_spectrogram()
# Makes a given music file (.wav) into a spectrogram and saves it as a png.
def make_spectrogram(file_name, png_dir):
    # sample_rate, samples = wavfile.read(file_name)
    # frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
    # plt.pcolormesh(times, frequencies, np.log(spectrogram))
    # plt.show()


    sample_rate, samples = wavfile.read(file_name)
    figure = specgram(samples, Fs=sample_rate, xextent=(0,30))
    frame1 = plt.gca()
    fig = plt.gcf()
    # NOTE: This is inspired from original size of 483x356 images. 483 / 200 = 2.415
    fig.set_size_inches(2.415, 1.78)

    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    base_name = os.path.basename(file_name).strip(".wav")

    # Saving the figure while removing white space border
    # NOTE: If you want smaller pictures, reduce the dpi.
    plt.savefig(os.path.join(png_dir,base_name + ".png"), bbox_inches='tight', pad_inches=-0.1, dpi=100)


# gen_music_file_names()
# Generating the full list of all music files in our code repo. Takes .au files
# and puts them into a list of absolute file paths.
def gen_music_file_names(au_file_dir):
    music_file_names = []
    for directory in os.listdir(au_file_dir):
        if os.path.isdir(os.path.join(au_file_dir,directory)):
            for file in os.listdir(os.path.join(au_file_dir,directory)):
                full_path = os.path.join(au_file_dir,directory,file)
                if full_path.endswith(".au"):
                    music_file_names.append(full_path)
    return music_file_names


if __name__ == "__main__":
    main()
