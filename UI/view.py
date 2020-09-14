from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5 import QtMultimedia as M
from strUP import Ui_Dialog
import sys
import os
from model import Model
import matplotlib.pyplot as plt
ppath= os.path.dirname(os.getcwd())
os.chdir(ppath)
xpath = os.getcwd() + '/Digital Signals Processing'
sys.path.insert(0, xpath)
from vqt import AMT

os.chdir(os.getcwd() + '/Model')


class MainWindowUIClass ( Ui_Dialog ) :
    def __init__(self) :

        super ( ).__init__ ( )
        self.model = Model ( )
        self.player = M.QMediaPlayer()
        self.player.positionChanged.connect ( self.moveSlider )
        self.player.durationChanged.connect(self.span)


    def setupUi(self, MW) :

        super ( ).setupUi ( MW )

        self.splitter.setSizes ( [300, 0] )

    def debugPrint(self, msg) :
        self.debugTextBrowser.append ( msg )

    # slot

    def span(self, duration):
        self.horizontalSlider.setRange(0, duration)


    def moveSlider(self, pos):
        self.horizontalSlider.setValue(pos)

    def stopAudio(self) :
        self.player.pause ( )

    # slot
    def transribeSlot(self) :
        ''' Called when the user presses the Write-Doc button.
        '''
       # self.model.transribe ( self.textEdit.toPlainText ( ) )
       # self.debugPrint ( "Transcrib" )
        self.url = QtCore.QUrl.fromLocalFile(self.model.getFileName())
        self.content = M.QMediaContent(self.url)
        AMT(self.model.getFileName())
        res = self.model.gtruthvector()
        self.player.setMedia(self.content)
        self.player.play()
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
            self.debugPrint ( "Transcribing: " + os.path.basename(fileName))
            self.model.setFileName ( fileName )



def main() :

    app = QtWidgets.QApplication ( sys.argv )
    MainWindow = QtWidgets.QMainWindow ( )
    ui = MainWindowUIClass ( )
    ui.setupUi ( MainWindow )
    MainWindow.show ( )
    sys.exit ( app.exec_ ( ) )

main ( )
