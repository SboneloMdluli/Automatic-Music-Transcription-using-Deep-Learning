import sys
import os
import execnet
import execnet
import pickle
import io
import numpy as np
import json


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

    def call_python_version(self,Version, Module, Function, ArgumentList) :
        gw = execnet.makegateway ( "popen//python=python%s" % Version )
        channel = gw.remote_exec ( """
            from %s import %s as the_function
            channel.send(the_function(*channel.receive()))
        """ % (Module, Function) )
        channel.send ( ArgumentList )
        return channel.receive ( )


    def gtruthvector(self):
        result = self.call_python_version ( "2.7", "onehotenc", "getHotVector",
                                   [self.getFileName(), 31.25, 20] )
        memfile = io.BytesIO ( )
        memfile.write ( json.loads ( result ).encode ( 'latin-1' ) )
        memfile.seek ( 0 )
        a = np.load ( memfile )
        return a