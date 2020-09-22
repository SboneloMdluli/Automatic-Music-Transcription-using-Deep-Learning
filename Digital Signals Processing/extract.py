import numpy as np 
import h5py
from glob import glob
import os

def loadData():
    '''
    # Looking h5 format data
    data_dir = os.getcwd()
    model_files = glob(data_dir + '*/.py')
    
    print(data_dir)
    print(len(model_files))
    '''
    filename = 'VQT.h5'
    path = os.getcwd() + '/' + filename 
    
    with h5py.File(path,'r') as hdf:
        ls = list(hdf.keys())
        print("List of datasets on the file: \n", ls)
        data = hdf.get('VQT_audio_frames')
        VQT_model_input = np.array(data)
                
    return VQT_model_input
        
loadData()
