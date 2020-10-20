import sys
import os
#import execnet
import pickle
import io
import numpy as np
import json
ppath= os.path.dirname(os.getcwd())
os.chdir(ppath)
xpath = os.getcwd() + '/Digital Signals Processing'
sys.path.insert(0, xpath)
from vqt import AMT
from model_input import AMT_Framing
xpath = os.getcwd() + '/Model'
sys.path.insert(0, xpath)
from notes import getnotes
from transmodel import onehotnotes
from numpy import savetxt
import os

class Model :
    def __init__(self) :
        self.fileName = None
        self.fileContent = ""

    def isValid(self, fileName) :

        try :
            file = open ( fileName, 'rb' )
            file.close ( )
            return True
        except :
            return False

    def setFileName(self, fileName) :

        if self.isValid ( fileName ) :
            self.fileName = fileName
            self.fileContents = open ( fileName, 'rb' ).read ( )
        else :
            self.fileContents = ""
            self.fileName = ""

    def getFileName(self) :
        return self.fileName

    def getFileContents(self) :

        return self.fileContents


    def transcribe(self):
        x = self.getFileName()+'.csv'
        hotvectors = np.empty([88,625])
        if os.path.exists(x):
            hotvectors = np.loadtxt(x, delimiter=",")
            
        AMT(self.getFileName()) # produce spectogram
        windows_ = AMT_Framing(self.getFileName())
        windows_ = windows_.reshape(windows_.shape[0:3])
        hotvectors = np.round(onehotnotes(windows_)) #transciption model
        hotvectors = hotvectors.reshape(hotvectors.shape[0:2])
        savetxt(x, hotvectors, delimiter=',')
        notes = getnotes(hotvectors)
        return notes