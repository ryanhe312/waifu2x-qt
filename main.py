import sys
import os

from PySide6.QtWidgets import QMainWindow,QApplication,QFileDialog,QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from ui import Ui_MainWindow
from engine import Client_Engine, resource_path

class Client_View(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path('logo.ico')))
        self.show()

        self.about = QMessageBox(self);
        self.about.setWindowTitle('About')
        self.about.setTextFormat(Qt.MarkdownText)
        self.about.setText('The source code can be accessed at [waifu2x-qt](https://github.com/ryanhe312/waifu2x-qt).'
                           'The SRCNN engine is from [waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan).\n'
                           'The Real-ESRGAN engine is from [Real-ESRGAN-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan).\n'
                           'The GUI is built with [Pyside6](https://doc.qt.io/qtforpython/).\n'
                           'LICENSES APPLIED.')

        self.inputOpen = QFileDialog(self)
        self.inputOpen.setAcceptMode(QFileDialog.AcceptOpen)
        self.inputOpen.setFileMode(QFileDialog.ExistingFiles)
        self.inputOpen.setWindowTitle('Select Open Path')
        self.inputOpen.setDirectory(os.getcwd())
        self.inputOpen.setNameFilter('Image Files(*.jpg *.png *.webp)')

        self.outputOpen = QFileDialog(self)
        # self.outputOpen.setAcceptMode(QFileDialog.AcceptSave)
        self.outputOpen.setFileMode(QFileDialog.Directory)
        self.outputOpen.setWindowTitle('Select Save Path')
        self.outputOpen.setDirectory(os.getcwd())

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = [i.toString()[8:] for i in event.mimeData().urls()]
        self.InputEdit.setText(','.join(urls))
        self.OutputEdit.setText(os.path.dirname(urls[0]))

class Client(object):
    def __init__(self,view:Client_View,engine:Client_Engine):
        self.view=view
        self.engine=engine
        self.view.Generate.clicked.connect(self.generate)
        self.view.Cancel.clicked.connect(self.cancel)
        self.view.About.clicked.connect(self.about)
        self.view.InputButton.clicked.connect(self.openInput)
        self.view.OutputButton.clicked.connect(self.openOutput)
        self.engine.status.connect(self.status)
#         self.log = open('log.txt','w')

    def openInput(self):
        self.status('[INFO] Open Input File.')
        if self.view.inputOpen.exec():
            input_path = self.view.inputOpen.selectedFiles()
            self.view.InputEdit.setText(','.join(input_path))
            self.view.OutputEdit.setText(os.path.dirname(input_path[0]))
            

    def openOutput(self):
        self.status('[INFO] Open Output File.')
        if self.view.outputOpen.exec():
            self.view.OutputEdit.setText(self.view.outputOpen.selectedFiles()[0])

    def generate(self):
        self.status('[INFO] Generate.')
        param = {
            'model': 'SRCNN' if self.view.ModelSRCNN.isChecked() else 
                     'RealESRGAN',
            'SRCNN': 'models-cunet' if self.view.SRCNNcunet.isChecked() else 
                     'models-upconv_7_anime_style_art_rgb' if self.view.SRCNNanime.isChecked() else
                     'models-upconv_7_photo',
            'RealESRGAN':
                     'realesrgan-x4plus' if self.view.realesrganx4plus.isChecked() else
                     'realesrnet-x4plus' if self.view.realesrnetx4plus.isChecked() else
                     'realesrgan-x4plus-anime',
            'noise': self.view.DenoiseSlider.value(),
            'scale':   self.view.ScaleSlider.value(),
            'input':   self.view.InputEdit.text().split(','),
            'output':   self.view.OutputEdit.text(),  
            'open': self.view.OpenImage.isChecked()      
        }
#         print(param,file=self.log, flush=True)

        # sanity check
        if len(param['input'])<1 or len(param['output'])<1:
            self.status('[ERROR] Please provide non-empty paths.')
            return

        self.engine.param={'total':len(param['input'])}
        self.engine.do_generate(param)

    def cancel(self):
        self.status('[INFO] Cancel.')
        self.engine.do_cancel()

    def about(self): 
        self.status('[INFO] About.')
        self.view.about.exec()

    def status(self,status):
#         print(status,file=self.log, flush=True)
        self.view.statusbar.showMessage(status)
        


if __name__=='__main__':
    app = QApplication(sys.argv)
    view = Client_View()
    engine = Client_Engine()
    client = Client(view,engine)
    sys.exit(app.exec())
