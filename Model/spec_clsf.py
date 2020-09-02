import keras.models import Sequential
import keras.layers import Conv2D, MaxPooling2D, Activation, Droupout, Flatten, Dense
import keras import backend as K
from keras.preprocessing image
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

im_Height, im_Width = 128, 1034
trainig_dir = ''
traingSample =  # size of training data 50%

validation_dir = ''
validSample =  # size of validation data 25 %

testing_dir = ''
testingSample =  # 25%


num_epochs = 50


# dimensions of image
if K.image_data_format() == 'channels_first':
  input_shape = (3,im_Width,im_Height)
else:
  input_shape = (im_Width,im_Height,3)


datagen = ImageDataGenerator()

batch_size = 10

train_data = datagen.flow_from_directory(trainig_dir, class_mode='binary', batch_size)

val_data = datagen.flow_from_directory(validation_dir, class_mode='binary', batch_size)

test_data = datagen.flow_from_directory(testing_dir, class_mode='binary', batch_size)


#model definition

model = Sequential()

model.add(Conv2D(32,(3,3)),input_shape)
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size(2,2)))

model.add(Conv2D(32,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size(2,2)))

model.add(Conv2D(32,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size(2,2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.summary()

model.compile(loss='binary_crossentropy',optimizer= 'adam',metrics=['accuracy'])

#train model

model.fit(train_data, steps_per_epoch=traingSample//batch_size,epochs=num_epochs,validation_data=val_data,
          validation_steps=validSample,)

#save model
model.save_weights('instruclasf.h5')

#check model
impath = ''

im_pred = image.load_img(impath) #test with piano
im_pred = image.img_to_array(im_pred)
im_pred = np.array([im_pred])

res = model.predict(im_pred)

if res[0][0]:
  print('piano')
else:
  print('drum')
