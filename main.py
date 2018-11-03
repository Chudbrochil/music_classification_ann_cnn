import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import numpy as np
import os
from matplotlib.pyplot import specgram
import matplotlib


def main():

    base_dir = "/home/anthony/git/music_classification_lstm_rnn"
    # Training
    split_size = 10
    au_dir = base_dir + "/genres"
    wav_dir = base_dir + "/split_" + str(split_size) + "/wavfiles"
    png_dir = base_dir + "/split_" + str(split_size) + "/pngfiles"
    # Validation
    #au_dir = base_dir + "/validation"
    #wav_dir = base_dir + "/split_" + str(split_size) + "/validation_wavfiles"
    #png_dir = base_dir + "/split_" + str(split_size) + "/validation_pngfiles"

    # Get all the base file names
    music_file_names = gen_music_file_names(au_dir)

    # Converting all our .au files to .wav files
    convert_to_wav(music_file_names, wav_dir, split_size)

    cleanup_last_file(wav_dir, split_size)

    # Take all the wav files and make them into pictures.
    for wav_file in os.listdir(wav_dir):
       make_spectrogram(os.path.join(wav_dir, wav_file), png_dir)


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
                list_of_files.append(os.path.join(pre_path, file))
        elif os.path.isfile(pre_path):
            list_of_files.append(pre_path)

    # Figuring out which files we should be returning
    for file in list_of_files:
        # If single_file is specified (i.e. "blues.00000"),
        # then this will only process that file.
        if file.endswith(".au") and single_file in file:
            music_file_names.append(file)

    return music_file_names


# convert_to_wav()
# Converts a given list of music filename's into wav files.
def convert_to_wav(music_file_names, wav_dir, split_size):
    for music_file_name in music_file_names:
        raw_file_name = (".".join(music_file_name.split(".")[0:2])).split("/")[-1]
        output_file_name = os.path.join(wav_dir, raw_file_name) + "-.wav"

        print("Output wav file: \n%s" % output_file_name)

        # Splitting the 30s wav into 10 3s wav's
        # Read "man sox" for more information on the command that is ran here.
        os.system("sox -e signed-integer " + music_file_name + " " + output_file_name + \
                  " trim 0 " + str(split_size) + " : newfile : restart")


# cleanup_last_file()
# When we make our clips and split them sometimes there will be a tiny
# last file that is made (usually is .1s or something). This method cleans up
# that last degenerate file.
def cleanup_last_file(wav_dir, split_size):

    # This index string will look like "-011"
    index_we_dont_want = int(30 / split_size) + 1
    index_string = "-0" + str(index_we_dont_want)

    for file in os.listdir(wav_dir):
        full_path = os.path.join(wav_dir,file)
        if index_string in full_path:
            os.system("rm " + full_path)


# make_spectrogram()
# Makes a given music file (.wav) into a spectrogram and saves it as a png.
def make_spectrogram(file_name, png_dir):

    print("Making spectrogram for file_name: \n%s" % file_name)
    sample_rate, samples = wavfile.read(file_name)
    #figure = specgram(samples, Fs=sample_rate, xextent=(0,30)) # NOTE: Old spectrogram...
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
    normalize = matplotlib.colors.Normalize(vmin = -10, vmax = 10)
    plt.pcolormesh(times, frequencies, np.log(spectrogram), norm=normalize, cmap='gray')
    frame1 = plt.gca()
    fig = plt.gcf()
    # NOTE: This is inspired from original size of 483x356 images. 483 / 200 = 2.415
    fig.set_size_inches(2.415, 1.78)

    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)

    # Saving the figure while removing white space border
    # NOTE: If you want smaller pictures, reduce the dpi.
    base_name = (os.path.basename(file_name))[:-4]
    plt.savefig(os.path.join(png_dir, base_name + ".png"), bbox_inches='tight',
                pad_inches=-0.1, dpi=100)

    plt.close()


if __name__ == "__main__":
    main()
