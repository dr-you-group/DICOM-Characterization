# Install PyInstaller and necessary packages
pip install pyinstaller pydicom PyQt5

# Execute PyInstaller
pyinstaller --onefile --windowed main.py --hidden-import pydicom.encoders.gdcm --hidden-import pydicom.encoders.pylibjpeg
