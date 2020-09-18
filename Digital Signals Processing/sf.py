# View Spectrogram of the Audio File..
# Importing General Packages
import numpy as np
import skimage                # Saving the spectrogram image
import skimage.io
import librosa
import librosa.display
from glob import glob
import os
import math

# Define Variable Q-Transform Parameters for Audio Signals Processing
fs = 44100  # Sampling frequency
hop_length = 512  # number of samples between successive VQT columns
fmin = None  # Minimum frequency. Defaults to C1 ~= 32.70 Hz
n_bins = 84  # Number of frequency bins
# Bandwidth offset for determining filter lengths (If Gamma=0 then => CQT computation)
gamma = 20
bins_per_octave = 12  # Number of frequency bins per octave
# Tuning offset in fractions of a bin(None, tuning will be automatically estimated from the signal)
tuning = 0.0
# Filter scale factor. Small values (<1) use shorter windows for improved time resolution.
filter_scale = 1
norm = 1  # Type of norm to use for basis function normalization
sparsity = 0.01  # Sparsify the VQT basis by discarding up to sparsity fraction of the energy
window = 'hann'  # Using Hann Window
scale = True  # Scale the VQT response by square-root the length of each channel’s filter
pad_mode = 'reflect'  # Padding mode for centered frame analysis
res_type = None  # The resampling mode for recursive downsampling
dtype = None  # The dtype of the output array. By default, this is inferred to match the numerical precision of the input signal
n_mels = 128
window_size = 7 # WINDOW_FRAME SIZE 
DURATION = 12
WINDOW_SIZE = 7

def scale_minmax(X, Xmin=0.0, Xmax=1.0):
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std * (Xmax - Xmin) + Xmin
    return X_scaled

def AMT():
    # Audio Processing
    # Loading the Audios
    # Path Configuration
    # path = os.getcwd() + '/' + filename_
    #path = os.getcwd()
    # filename = "{}".format(filename_)
    filename = 'Guns N Roses-Sweet Child O Mine Intro.wav'
    x, fs = librosa.load(filename, sr=None, mono=True, duration=DURATION)
    V= librosa.vqt(x, sr=fs, hop_length=hop_length, fmin=fmin, n_bins=n_bins, gamma=20, bins_per_octave=bins_per_octave, tuning=tuning,
                        filter_scale=filter_scale, norm=norm, sparsity=0.01, window='hann', scale=scale, pad_mode=pad_mode, res_type=res_type, dtype=dtype)
    #VQT_result = np.absolute(V)
    V_mel = np.abs(V)  # Mapping Magnitude spectrogram to the Mel Scale
    logFrame = librosa.amplitude_to_db(V_mel)
    #librosa.display.specshow(logFrame ,sr=fs, x_axis='time', y_axis='mel', fmin=fmin, fmax=8000, cmap="coolwarm")
    mels = librosa.feature.melspectrogram( S=V_mel, sr=fs, n_mels=n_mels, n_fft=hop_length*2, hop_length=hop_length)
    # Smels = librosa.display.specshow(mels, sr=fs, x_axis='time', y_axis='mel', fmin=fmin, fmax=8000, cmap="coolwarm")
    
    np_array_list = []
    np_array_list.append(mels)    
    combined = np.concatenate(np_array_list, axis = 1)
    mean = np.mean(combined, axis = 1, keepdims =True)
    std = np.std(combined, axis = 1, keepdims=True)
    
    for i in range(len(np_array_list)):
        np_array_list[i] = np.divide(np.subtract(np_array_list[i], mean), std)
   
    frame_windows_list = []
    numSlices_list = []
    Y_numSlices = 625
    
    for i in range(len(np_array_list)):
        VQT_result = np_array_list[i]
        paddedX = np.zeros((VQT_result.shape[0], VQT_result.shape[1] + WINDOW_SIZE - 1), dtype=float)
        pad_amount = int(WINDOW_SIZE / 2)
        paddedX[:, pad_amount:-pad_amount] = VQT_result
        frame_windows = np.array([paddedX[:, j:j+WINDOW_SIZE] for j in range(VQT_result.shape[1])])
        frame_windows = np.expand_dims(frame_windows, axis=3)
        numSlices = min(frame_windows.shape[0],Y_numSlices)
        numSlices_list.append(numSlices)
        frame_windows_list.append(frame_windows[:numSlices]) 
        combined2 = np.concatenate(frame_windows_list, axis=0)
    
    # return np.concatenate(frame_windows_list, axis=0), numSlices_list 
    # result = combined2[0][1]
    result = combined2[450][127]
    print(result)
    librosa.display.specshow(result ,sr=fs, x_axis='time', y_axis='mel', fmin=fmin, fmax=8000, cmap="coolwarm")
'''    
    # Attempt at displaying each spectrogram
    # for 
#def spectrograms():
    
     

     #print (frame_windows_list[i])
        logFrame = librosa.amplitude_to_db(np.abs(frame_windows_list[i]))
        librosa.display.specshow(logFrame, sr=fs, x_axis='time', y_axis='cqt_note', fmin=fmin, cmap='coolwarm')
        
        #Smels = librosa.display.specshow(frames_windows_list[i], sr=fs, x_axis='time', y_axis='mel', fmin=fmin, fmax=8000, cmap="coolwarm")
  
def melScale():
    12*31.25 = number of frames;
    
    # Conversion into the Mel-Scale to display and save Mel-spectrogram
    V_mel = np.abs(V)  # Mapping Magnitude spectrogram to the Mel Scale
    mels = librosa.feature.melspectrogram(
    S=V_mel, sr=fs, n_mels=n_mels, n_fft=hop_length*2, hop_length=hop_length)
    #Smels = librosa.display.specshow(mels, sr=fs, x_axis='time', y_axis='mel', fmin=fmin, fmax=8000, cmap="coolwarm")

    # CONVERSION
    mels = np.log(mels + 1e-9)  # add small number to avoid log(0)
    out = "{}.png".format(filename)

    # min-max scale to fit inside 8-bit range
    img = scale_minmax(mels, 0, 255).astype(np.uint8)
    # put low frequencies at the bottom in image
    img = np.flip(img, axis=0)
    img = 255-img  # invert. make black==more energy

    # save as PNG
    skimage.io.imsave(out, img)
    '''    
AMT()