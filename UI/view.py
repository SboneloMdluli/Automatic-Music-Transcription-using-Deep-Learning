from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5 import QtMultimedia as M
from amtui import Ui_Dialog
import sys
from model import Model


class MainWindowUIClass ( Ui_Dialog ) :
    def __init__(self) :

        super ( ).__init__ ( )
        self.model = Model ( )

    def setupUi(self, MW) :

        super ( ).setupUi ( MW )

        self.splitter.setSizes ( [300, 0] )

    def debugPrint(self, msg) :
        self.debugTextBrowser.append ( msg )

    def refreshAll(self) :

        self.lineEdit.setText ( self.model.getFileName ( ) )
        self.textEdit.setText ( self.model.getFileContents ( ) )

    # slot
    def returnedPressedSlot(self) :

        fileName = self.lineEdit.text ( )
        if self.model.isValid ( fileName ) :
            self.model.setFileName ( self.lineEdit.text ( ) )
            self.refreshAll ( )
        else :
            m = QtWidgets.QMessageBox ( )
            m.setText ( "Invalid file name!\n" + fileName )
            m.setIcon ( QtWidgets.QMessageBox.Warning )
            m.setStandardButtons ( QtWidgets.QMessageBox.Ok
                                   | QtWidgets.QMessageBox.Cancel )
            m.setDefaultButton ( QtWidgets.QMessageBox.Cancel )
            ret = m.exec_ ( )
            self.lineEdit.setText ( "" )
            self.refreshAll ( )
            self.debugPrint ( "Invalid file specified: " + fileName )

    # slot
    def transribeSlot(self) :
        ''' Called when the user presses the Write-Doc button.
        '''
       # self.model.transribe ( self.textEdit.toPlainText ( ) )
       # self.debugPrint ( "Transcrib" )
        self.url = QtCore.QUrl.fromLocalFile(self.model.getFileName())
        self.content = M.QMediaContent(self.url)
        self.player = M.QMediaPlayer()
        self.player.setMedia(self.content)
        self.player.play()


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
            self.debugPrint ( "setting file name: " + fileName )
            self.model.setFileName ( fileName )
            self.refreshAll ( )


def main() :

    app = QtWidgets.QApplication ( sys.argv )
    MainWindow = QtWidgets.QMainWindow ( )
    ui = MainWindowUIClass ( )
    ui.setupUi ( MainWindow )
    MainWindow.show ( )
    sys.exit ( app.exec_ ( ) )


main ( )
