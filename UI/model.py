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

    def transribe(self, text) :
        pass
