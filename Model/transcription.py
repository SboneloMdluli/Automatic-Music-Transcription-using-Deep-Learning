from keras.models import Sequential
from keras.callbacks import Callback, ModelCheckpoint
import keras.backend as K
import numpy as np
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.layers import LSTM, Bidirectional, Dense
from numpy import random

model = Sequential()                                                            
"""
model.add(Conv2D(filters=50,kernel_size=(25,5),padding="same",input_shape=(252, 7, 1)))  # octaves*bins, frames, channels
model.add(Activation('tanh'))                                                   
model.add(MaxPooling2D(pool_size=(3,1)))
model.add(Dropout(0.2))

model.add(Conv2D(filters=50,kernel_size=(5,3),padding="same",input_shape=(252, 7, 1)))
model.add(Activation('sigmoid'))                                                   
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))                                        

model.add(Flatten())
model.add(Dense(units=200,activation='sigmoid'))
model.add(Dropout(0.2))
model.add(Dense(units=200,activation='sigmoid'))
model.add(Dropout(0.2))
model.add(Dense(88))   # number of notes                                                          
"""

X = list ( )
Y = list ( )
X = [x for x in range ( 5, 301, 5 )]

X = np.array ( X ).reshape ( 20, 3, 1 ).astype ( np.float32 )

Y = random.choice ( [0, 1], size=(20, 3, 1) ).astype ( np.float32 )

# model definition
model = Sequential ( )
model.add ( Bidirectional ( LSTM ( 100, activation='relu', input_shape=(3, 1) ) ) )
model.add ( RepeatVector ( 3 ) )
model.add ( Bidirectional ( LSTM ( 100, activation='relu', return_sequences=True ) ) )
model.add ( TimeDistributed ( Dense ( 1, activation='sigmoid' ) ) )

def get_f1(y_true, y_pred) :
    true_positives = K.sum ( K.round ( K.clip ( y_true * y_pred, 0, 1 ) ) )
    possible_positives = K.sum ( K.round ( K.clip ( y_true, 0, 1 ) ) )
    predicted_positives = K.sum ( K.round ( K.clip ( y_pred, 0, 1 ) ) )
    precision = true_positives / (predicted_positives + K.epsilon ( ))
    recall = true_positives / (possible_positives + K.epsilon ( ))
    f1_val = 2 * (precision * recall) / (precision + recall + K.epsilon ( ))
    return f1_val

model.compile ( loss='binary_crossentropy', optimizer='adam', metrics=[get_f1] )

history = model.fit ( X, Y, epochs=1000, validation_split=0.2, verbose=1, batch_size=3 )

model.summary ( )

test_input = np.array ( [300, 305, 310] )
test_input = test_input.reshape ( (1, 3, 1) )
print ( test_input )

test_output = model.predict ( test_input, verbose=0 )
print ( test_output )

# save model
# model.save('trans.h5')