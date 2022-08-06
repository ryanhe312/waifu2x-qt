import os
import sys

from PySide6.QtCore import QObject, Signal, QProcess, QUrl, QWaitCondition, QMutex
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
        self.process = QProcess()
        self.process.readyReadStandardError.connect(self.do_read)
        self.process.finished.connect(self.do_finish)
        self.process.errorOccurred.connect(self.do_error)
        self.param = {'total':0}

    def do_generate(self, param):
        self.param.update(param)

        # print(param['input'])
        # print(param['output'])

        if len(self.param['input'])<1: 
            if self.param['open'] and self.param['output']:
                QDesktopServices.openUrl(QUrl(f"file:///{param['output']}",QUrl().TolerantMode))
            return

        input_path = self.param['input'][0]
        self.param['input'] = self.param['input'][1:]

        basename = os.path.basename(input_path)
        form = basename.split('.')[-1]
        output_path = basename[:-len(form)-1]+'_waifu2x.'+form
        output_path = os.path.join(param['output'], output_path)

        if param['model'] == 'SRCNN':
            engine = srcnn_path
            args = [f" -m \"{os.path.join(srcnn_model_path,param['SRCNN'])}\"" ,
                    f" -i \"{input_path}\" ",
                    f" -o \"{output_path}\" ",
                    f" -s {2**param['scale']}",
                    f" -n {param['noise']}"]
        
        else:
            engine = realesrgan_path
            args = [f" -m \"{realesrgan_model_path}\" ",
                    f" -n {param['RealESRGAN']} " ,
                    f" -i \"{input_path}\" ",
                    f" -o \"{output_path}\" ",
                    f" -s 4"]

        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] "+f"\"{engine}\""+' '.join(args))
        self.process.startCommand(f"\"{engine}\""+' '.join(args))

    def do_finish(self):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] Finished with {len(self.param['input'])} left.")
        self.do_generate(self.param)

    def do_error(self):
        self.status.emit("[ERROR] Process failed:"+ self.process.errorString())

    def do_read(self):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] "+self.process.readAllStandardError().data().decode().strip())

    def do_cancel(self):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] Trying kill process.")
        self.process.kill()
        self.process.terminate()
