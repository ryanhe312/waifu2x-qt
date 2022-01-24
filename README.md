# waifu2x-qt

This tool allows you to magnify your image with smoothing, especially for anime screenshots and illustrations.

(1) Set your input path and output path in Files Panel. Please use same file extensions for input and output.

(2) Select your preferred engine and parameters in Configs Panel. (staying default is recommended)

(3) Click Generate in Action Panel and wait for several minutes to process. 

## Run

1. download waifu2x and real-esrgan package
```
wget https://github.com/nihui/waifu2x-ncnn-vulkan/releases/download/20210521/waifu2x-ncnn-vulkan-20210521-windows.zip
unzip waifu2x-ncnn-vulkan-20210521-windows.zip
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.3.0/realesrgan-ncnn-vulkan-20211212-windows.zip
unzip realesrgan-ncnn-vulkan-20211212-windows.zip
```

2. prepare python environment
```
pip install PySide6
```

3. run the main.py

## Build

1. prepare python environment
```
pip install PyInstaller
```

2. build package
```
pyinstaller --onefile --windowed --icon=logo.ico main.py
```

## LICENSE

The source code can be accessed at [waifu2x-qt](https://github.com/ryanhe312/waifu2x-qt).
The SRCNN engine is from [waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan).
The Real-ESRGAN engine is from [Real-ESRGAN-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan).
The GUI is built with [Pyside6](https://doc.qt.io/qtforpython/).

LICENSES APPLIED.
