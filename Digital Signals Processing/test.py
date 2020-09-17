import librosa
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import glob
from random import shuffle

DURATION = 12
DOWNSAMPLED_SR = 16000
HOP_LENGTH = 512
NUM_OCTAVES = 7
BINS_PER_OCTAVE = 36
NUM_BINS = NUM_OCTAVES * BINS_PER_OCTAVE
WINDOW_SIZE = 7

def preprocess_wav_file(files, Y_numSlices):
    # returns 1 example (downsampled, cqt, normalized)
    np_array_list = []
    filename = 'Guns N Roses-Sweet Child O Mine Intro.wav'
    y, sr = librosa.load(filename, sr = None, duration=DURATION)
    y_downsample = librosa.resample(y, orig_sr=sr, target_sr=DOWNSAMPLED_SR)
    CQT_result = librosa.cqt(y_downsample, sr=DOWNSAMPLED_SR, hop_length=HOP_LENGTH, n_bins=NUM_BINS, bins_per_octave=BINS_PER_OCTAVE)
    CQT_result = np.absolute(CQT_result)
    np_array_list.append(CQT_result)

    combined = np.concatenate(np_array_list, axis = 1)
    mean = np.mean(combined, axis = 1, keepdims =True)
    std = np.std(combined, axis = 1, keepdims=True)
    for i in range(len(np_array_list)):
        np_array_list[i] = np.divide(np.subtract(np_array_list[i], mean), std)

    frame_windows_list = []
    numSlices_list = []
    for i in range(len(np_array_list)):
        CQT_result = np_array_list[i]
        paddedX = np.zeros((CQT_result.shape[0], CQT_result.shape[1] + WINDOW_SIZE - 1), dtype=float)
        pad_amount = WINDOW_SIZE / 2
        paddedX[:, pad_amount:-pad_amount] = CQT_result
        frame_windows = np.array([paddedX[:, j:j+WINDOW_SIZE] for j in range(CQT_result.shape[1])])
        frame_windows = np.expand_dims(frame_windows, axis=3)
        numSlices = min(frame_windows.shape[0],Y_numSlices[i])
        numSlices_list.append(numSlices)
        frame_windows_list.append(frame_windows[:numSlices])
    return np.concatenate(frame_windows_list, axis=0), numSlices_list

def get_wav_midi_data(filenames):
    X_filenames = []
    Y_numSlices = []
    Y_list = []
    for wav_file, midi_file in filenames:
        X_filenames.append(wav_file)
        Y_i = preprocess_midi_truth(midi_file)
        Y_numSlices.append(Y_i.shape[1])
        Y_list.append(Y_i)

    X, numSlices = preprocess_wav_file(X_filenames, Y_numSlices)
    Y_list = [Y_list[i][:,:numSlices[i]] for i in range(len(Y_list))]
    Y = np.concatenate(Y_list, axis=1)
    Y = [Y[i] for i in range(Y.shape[0])]
    return X, Y

def main():    
    filenames = getFileList()
    print ("Number of Songs: {}".format(len(filenames)))
    X, Y = get_wav_midi_data(filenames)
    print ("Number of Training Examples: {}".format(X.shape[0]))
    np.save("X_input_shuffled", X)
    np.save("Y_input_shuffled", Y)


if __name__ == "__main__":
    main()