# Automatic-Music-Transcription-using-Deep-Learning

<p align="center">
Sbonelo Mdluli and Moshekwa Malatji 
</p>


The repo contains the implemenation of an automatic music transcription application. Automatic music transcription is the process of converting music signal into musical notes.
The application transcribes 2 instruments which are:

  - Piano - channel 0
  - Drums - channel 9

### Representation

The application UI is developed using PyQt5. Which can be installed using the command below.
```sh
 pip install PyQt5
```

### Digital Signal Processing

The audio file are processed using variable Q-Transform. Digial signal processing is done using Librosa.
```sh
 pip install librosa
```

### Machine Learning
The instrument classification model in made using Keras which can be installed using.
```sh
 pip3 install --user --upgrade tensorflow 
 pip install Keras
```
#### Data preparation

[The ground truth data is generated using MIDI format](https://web.archive.org/web/20141227205754/http://www.sonicspot.com:80/guide/midifiles.html). We use [open source MIDI parser to get note data](https://mido.readthedocs.io/en/latest/index.html). [The Midi score to note mapping for a piano is a one to one mapping E.g {72=G#6, 67=D#6, 64=C6}](https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies)

### Application Executable
```sh
 pyinstaller --onefile view.py
```sh