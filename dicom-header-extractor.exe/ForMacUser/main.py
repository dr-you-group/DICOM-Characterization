import sys
import os
import argparse
import pydicom.encoders
from PyQt5.QtWidgets import QApplication, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLabel, QProgressBar
from find_dcm_files import find_dcm_files
from extract_dicom_header import extract_dicom_header
from deidentify import deidentify
from save_to_csv import save_to_csv

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('DICOM Metadata Extractor')
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()
        
        self.button_select_directory = QPushButton('Select Directory', self)
        self.button_select_directory.clicked.connect(self.showDirectoryDialog)
        layout.addWidget(self.button_select_directory)

        self.button_select_output = QPushButton('Select Output File', self)
        self.button_select_output.clicked.connect(self.showFileDialog)
        layout.addWidget(self.button_select_output)

        self.directory_label = QLabel('Selected Directory: ', self)
        layout.addWidget(self.directory_label)

        self.output_label = QLabel('Selected Output File: ', self)
        layout.addWidget(self.output_label)

        self.progress_label = QLabel('Progress: ', self)
        layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
    
    def showDirectoryDialog(self):
        self.directory = QFileDialog.getExistingDirectory(self, 'Select Directory', '/')
        self.directory_label.setText(f'Selected Directory: {self.directory}')
    
    def showFileDialog(self):
        if hasattr(self, 'directory'):
            self.output_file, _ = QFileDialog.getSaveFileName(self, 'Save CSV', '/', 'CSV Files (*.csv)')
            if self.output_file:
                self.output_label.setText(f'Selected Output File: {self.output_file}')
                self.extract_metadata()
    
    def extract_metadata(self):
        dcm_files = find_dcm_files(self.directory)
        total_files = len(dcm_files)
        current_progress = 0
        self.progress_bar.setMaximum(total_files)
        
        all_headers = []
        for idx, dicom_file in enumerate(dcm_files, start=1):
            header, sop_class_uid, study_uid, series_uid = extract_dicom_header(dicom_file)
            if deidentify_option:
                header = deidentify(header)
            all_headers.append({
                "File Name": dicom_file,
                "Header": header,
                "SOP Class UID": sop_class_uid,
                "Study UID": study_uid,
                "Series UID": series_uid
            })
            current_progress = idx
            self.progress_bar.setValue(current_progress)
            self.progress_label.setText(f'Progress: {current_progress}/{total_files}')
            QApplication.processEvents()  # Update the GUI
        
        save_to_csv(all_headers, self.output_file)
        self.progress_label.setText(f'Completed processing {total_files} files.')
        print(f"Metadata extraction and saving to CSV completed at {self.output_file}")

def load_config(config_file='config.txt'):
    config = {}
    with open(config_file, 'r') as file:
        for line in file:
            name, value = line.strip().split('=')
            config[name] = value
    return config

def parse_arguments():
    parser = argparse.ArgumentParser(description='DICOM Header Extractor')
    parser.add_argument('--directory', '-d', type=str, default='.', help='Directory to search for DICOM files')
    parser.add_argument('--deidentify', '-di', action='store_true', help='Deidentify DICOM tags')
    
    # Jupyter 노트북에서 실행 중인지 확인하고 인수를 무시합니다.
    if 'ipykernel' in sys.modules:
        args, unknown = parser.parse_known_args()
    else:
        args = parser.parse_args()
    
    return args

if __name__ == "__main__":
    args = parse_arguments()
    directory_to_search = args.directory
    deidentify_option = args.deidentify
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
