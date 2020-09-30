from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5 import QtMultimedia as M
from strUP import Ui_Dialog
import sys
import os
from model import Model
import time
import matplotlib.pyplot as plt

class MainWindowUIClass ( Ui_Dialog ) :
    def __init__(self) :

        super ( ).__init__ ( )
        self.model = Model ( )
        self.player = M.QMediaPlayer()
        self.player.positionChanged.connect ( self.moveSlider )
        self.player.durationChanged.connect(self.span)
        self.instrument = ''
        self.notes = ''


    def setupUi(self, MW) :

        super ( ).setupUi ( MW )

        self.splitter.setSizes ( [300, 0] )

    def debugPrint(self, msg) :
        self.debugTextBrowser.append ( msg )

    # slot

    def span(self, duration):
        self.horizontalSlider.setRange(0, duration)
        #print(duration)


    def moveSlider(self, pos):
        self.horizontalSlider.setValue(pos)

    def stopAudio(self) :
        self.player.pause ( )

    # slot
    def transribeSlot(self) :
        ''' Called when the user presses the Write-Doc button.
        '''
        self.url = QtCore.QUrl.fromLocalFile(self.model.getFileName())
        self.content = M.QMediaContent(self.url)
        notes = self.model.transcribe()
        self.notes = notes[0]
        self.instrument = notes[1]
        self.debugPrint("Instrument type :" + self.instrument)
        self.player.setMedia(self.content)
        self.player.play()

        for i in self.notes:
            self.debugPrint(i)
            #self.debugTextBrowser.clear()

        #plt.matshow ( res )
        #plt.show ( )


    # slot
    def browseSlot(self) :
        ''' Called when the user presses the Browse button
        '''
        # self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options ( )
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName (
            None,
            "QFileDialog.getOpenFileName()",
            "",
            "All Files (*)",
            options=options )
        if fileName :
            self.pushButton_2.setEnabled ( True )
            self.pushButton_3.setEnabled ( True )
            self.model.setFileName ( fileName )
            self.debugPrint("Transcribing: " + os.path.basename(fileName))



def main() :

    app = QtWidgets.QApplication ( sys.argv )
    MainWindow = QtWidgets.QMainWindow ( )
    ui = MainWindowUIClass ( )
    ui.setupUi ( MainWindow )
    MainWindow.show ( )
    sys.exit ( app.exec_ ( ) )

main ( )
