import os
import sys

from PySide6.QtCore import QObject, Signal, QProcess, QUrl
from PySide6.QtGui import QDesktopServices

def resource_path(*relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, *relative_path)

srcnn_path = resource_path('waifu2x','waifu2x-ncnn-vulkan.exe')
srcnn_model_path = resource_path('waifu2x')
realesrgan_path = resource_path('realesrgan','realesrgan-ncnn-vulkan.exe')
realesrgan_model_path = resource_path('realesrgan','models')

class Client_Engine(QObject):
    status = Signal(str)

    def __init__(self):
        super().__init__()
        self.openAfterProcess = True
        self.outputPath = ''
        self.process = QProcess()
        self.process.readyReadStandardError.connect(self.do_read)
        self.process.finished.connect(self.do_finish)
        self.process.errorOccurred.connect(self.do_error)

    def do_generate(self, param):
        self.openAfterProcess = param['open']
        self.outputPath = param['output']

        if param['model'] == 'SRCNN':
            engine = srcnn_path
            args = [f" -m {os.path.join(srcnn_model_path,param['SRCNN'])}" ,
                    f" -i {param['input']} ",
                    f" -o {param['output']} ",
                    f" -s {2**param['scale']}",
                    f" -n {param['noise']}"]
           
        else:
            engine = realesrgan_path
            args = [f" -m {realesrgan_model_path} ",
                    f" -n {param['RealESRGAN']} " ,
                    f" -i {param['input']} ",
                    f" -o {param['output']} ",
                    f" -s {2**param['scale']}"]

        self.status.emit('[INFO] '+engine+' '.join(args))
        self.process.startCommand(engine+' '.join(args))

    def do_finish(self):
        self.status.emit("[INFO] Finished.")
        if self.openAfterProcess and self.outputPath:
            QDesktopServices.openUrl(QUrl(f"file:///{self.outputPath}",QUrl().TolerantMode))

    def do_error(self):
        self.status.emit("[ERROR] Process failed:"+ self.process.errorString())

    def do_read(self):
        self.status.emit("[INFO] "+self.process.readAllStandardError().data().decode().strip())

    def do_cancel(self):
        self.status.emit("[INFO] Trying kill process.")
        self.openAfterProcess = False
        self.process.kill()
        self.process.terminate()