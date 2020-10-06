from keras.models import load_model
import os

def onehotnotes(windows):
    path = os.getcwd() + '/Model/seq2seq.h5' 
    #dependencies = { 'get_f1': get_f1 }
    model = load_model(path,compile=False)
    result = model.predict(windows)
    return result