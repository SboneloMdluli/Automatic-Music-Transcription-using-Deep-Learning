from keras.callbacks import Callback,ModelCheckpoint
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator,load_img,array_to_img,img_to_array
from keras.callbacks import Callback,ModelCheckpoint
from keras.wrappers.scikit_learn import KerasClassifier
import keras.backend as K
import numpy as np

im_Height, im_Width = 128, 1034                                                 
training_dir = '/content/drive/My Drive/spectrograms/train_data'                
trainingSample =  486 # size of training data 75%                               

validation_dir = '/content/drive/My Drive/spectrograms/validation'              
validSample = 69 # size of validation data 15 %                                 

testing_dir = '/content/drive/My Drive/spectrograms/test_data'                  
testingSample =  101  # 10 %                                                    

num_epochs = 50                                                                 
                                      

datagen = ImageDataGenerator(1/255)                                                  

batch_size = 10                                                                 

train_data = datagen.flow_from_directory(training_dir,target_size=(256,256),batch_size=10, class_mode='binary')
val_data = datagen.flow_from_directory(validation_dir,target_size=(256,256),batch_size=10, class_mode='binary')
test_data = datagen.flow_from_directory(testing_dir,target_size=(256,256), batch_size=10, class_mode='binary')

#model definition                                                               

model = Sequential()                                                            

model.add(Conv2D(filters=50,kernel_size=(25,5),input_shape=(252, 7, 1)))  # octaves*bins, frames, channels                       
model.add(Activation('tanh'))                                                   
model.add(MaxPooling2D(pool_size=(3,1)))
model.add(Dropout(0.2))


model.add(Conv2D(filters=50,kernel_size=(5,3),input_shape=(252, 7, 1)))                                                    
model.add(Activation('sigmoid'))                                                   
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))                                        
                                    

model.add(Flatten())
model.add(Dense(units=200,activation='sigmoid'))
model.add(Dropout(0.2))
model.add(Dense(units=200,activation='sigmoid'))
model.add(Dropout(0.2))
model.add(Dense(88))   # number of notes                                                          
                                
model.summary()


def get_f1(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

model.compile(loss='binary_crossentropy',optimizer= 'adam',metrics=[get_f1])

#train model

model.fit(train_data, steps_per_epoch=486//batch_size,epochs=50,validation_data=val_data,
          validation_steps=validSample)

#save model                                                                     
model.save('trans.h5')
