# View Spectrogram of the Audio File..
# Importing General Packages
import numpy as np
import skimage               
import skimage.io
import librosa
import librosa.display
from glob import glob
import os
import h5py
#from midi2audio import FluidSynth

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
DURATION = 12
WINDOW_SIZE = 7

def AMT_Framing(filename_):
    # Audio Processing
    #filename = 'Guns N Roses-Sweet Child O Mine Intro.wav'
    filename = "{}".format(filename_)
    x, fs = librosa.load(filename, sr=None, mono=True, duration=DURATION)
    V= librosa.vqt(x, sr=fs, hop_length=hop_length, fmin=fmin, n_bins=n_bins, gamma=0, bins_per_octave=bins_per_octave, tuning=tuning,
                        filter_scale=filter_scale, norm=norm, sparsity=0.01, window='hann', scale=scale, pad_mode=pad_mode, res_type=res_type, dtype=dtype)
    # Mapping Magnitude spectrogram to the Mel Scale
    V_mel = np.abs(V)  
    logFrame = librosa.amplitude_to_db(V_mel)
    mels = librosa.feature.melspectrogram( S=V_mel, sr=fs, n_mels=n_mels, n_fft=hop_length*2, hop_length=hop_length)
    
    np_array_list = []
    np_array_list.append(mels)    
    
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
    
    audio_frames= np.concatenate(frame_windows_list, axis=0)
    #storingData(audio_frames)
    #return audio_frames 

'''
#Function to store the frames in a hdf5 file    
def storingData(frames,filename):    
    filename = 'VQT.h5'
    path = os.getcwd() + '/' + filename
    with h5py.File(path,'w') as hdf:
        hdf.create_dataset('VQT_audio_frames',data=frames)
    
#AMT_Framing(filename)
#AMT_Framing()
'''