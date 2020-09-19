from glob import glob
import os

path = os.getcwd()
print(path)   # Check current directory path
#audio_files = glob(path + '/*.wav')     # Collect all wav format files
audio_files = glob(path + '/*.midi')     # Collect all .midi files(try mid
print(len(audio_files))  # Number of files

for filename in range(0,len(audio_files),1):
    #filename = "{}".format(filename_)
    audio_files[filename] # To index each file..example below
    #x, fs = librosa.load(audio_files[filename], sr=None, mono=True, duration=12)