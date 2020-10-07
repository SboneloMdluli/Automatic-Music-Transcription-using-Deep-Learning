from keras.models import Sequential
from keras.callbacks import Callback,ModelCheckpoint
import keras.backend as K
import numpy as np
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.layers import LSTM, Bidirectional, Dense
from numpy import random
from array import array
import numpy as np
import h5py

X = list()
Y = list()

#model definition                                                               
model = Sequential() 
model.add(Bidirectional(LSTM(200, activation='relu', input_shape=(128, 7)))) #  encoder
model.add(RepeatVector(88))
model.add(Bidirectional(LSTM(100, activation='relu', return_sequences=True))) #decoder
model.add(TimeDistributed(Dense(1)))                                     

def get_f1(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

model.compile(optimizer='adam', loss='categorical_crossentropy')


Y = np.loadtxt("/content/drive/My Drive/things/1_funk-groove1_138_beat_4-4.mid.csv",delimiter=",")

#X = random.choice([0,5], size=(625,128,7)).astype(np.float32)   #windows, batches, 7   (625,128,7)
#Y = random.choice([0,1], size=(625,88,1)).astype(np.float32)   #(625,88,1)

Y = Y.transpose()

filename = '/content/drive/My Drive/things/VQT.h5'
path = '/content/drive/My Drive/things/VQT.h5'

with h5py.File(path,'r') as hdf:
  ls = list(hdf.keys())
  #print("List of datasets on the file: \n", ls)
  data = hdf.get('VQT_audio_frames')
  X = np.array(data)*10


Y = Y.reshape((Y.shape[0], Y.shape[1], 1))

X = X.reshape(X.shape[0:3])

history = model.fit(X, Y, epochs=50, validation_split=0.2, verbose=1, batch_size=128)


model.summary()

test_input = X[402]

test_input = test_input.reshape((1,128, 7))
#print(test_input)

test_output = model.predict(test_input, verbose=0)
print(test_output)
