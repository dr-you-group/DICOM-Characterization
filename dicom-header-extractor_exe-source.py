import os
import pydicom
import zipfile
import tarfile
import shutil
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from PyQt5.QtWidgets import QApplication, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLabel, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt
import sys
import multiprocessing

# Check if a file is DICOM
def is_dicom_file(filepath):
    try:
        pydicom.dcmread(filepath, stop_before_pixels=True)
        return True
    except (pydicom.errors.InvalidDicomError, FileNotFoundError, IsADirectoryError, IOError, ValueError) as e:
        log_error(f"Invalid DICOM file format: {filepath}, error: {e}")
    except PermissionError as e:
        log_error(f"Permission denied: {filepath}, error: {e}")
    except Exception as e:
        log_error(f"Error reading DICOM file: {filepath}, error: {e}")
    return False

# Log errors to a file
def log_error(message):
    with open('error_log.txt', 'a') as log_file:
        log_file.write(f"{message}\n")

# Extract archives
def extract_archives(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if file.endswith('.zip'):
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(root)
                elif file.endswith(('.tar', '.tar.gz', '.tar.bz2')):
                    with tarfile.open(file_path, 'r') as tar_ref:
                        tar_ref.extractall(root)
            except Exception as e:
                log_error(f"Failed to extract archive: {file_path}, error: {e}")

# Find DICOM files and manage large files
def find_dcm_files(directory):
    dcm_files = []
    extract_archives(directory)

    unsupported_extensions = ['.ann', '.app', '.avi', '.bar', '.bmp', '.dat', '.dct', '.dcmtbn', '.dll', '.exe', '.gif', '.htm', '.html', '.ico', '.inf', 
                   '.ini', '.jpg', '.js', '.lda', '.mdb', '.msg', '.ocx', '.pal', '.png', '.pro', '.pwl', '.rst', '.rtf', '.sav', 
                   '.sm', '.ssm', '.srv', '.tbx', '.tby', '.txt', '.xls', '.xml', '.xpr', '.xsl', '.zom']  # Can expand this list for other unsupported formats
    max_workers = multiprocessing.cpu_count()  # Dynamically set the max workers based on CPU cores

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if any(file.lower().endswith(ext) for ext in unsupported_extensions):
                    print(f"Skipping unsupported file: {file_path}")
                    continue
                if file.lower().endswith('.dcm'):
                    if file_path not in dcm_files:  # Prevent adding duplicate files
                        dcm_files.append(file_path)
                else:
                    future = executor.submit(is_dicom_file, file_path)
                    futures[future] = file_path

        for future in as_completed(futures):
            file_path = futures[future]
            try:
                result = future.result()
                if result:
                    if file_path not in dcm_files:  # Prevent adding duplicate files
                        dcm_files.append(file_path)
            except Exception as e:
                log_error(f"Error processing file {file_path}: {e}")

    if not dcm_files:
        print("No DICOM files found. Exiting.")
        sys.exit(0)

    return dcm_files

# Extract DICOM headers
def extract_dicom_header(dicom_file):
    pydicom.config.convert_wrong_length_to_UN = True
    try:
        ds = pydicom.dcmread(dicom_file, force=True)
    except (FileNotFoundError, IOError) as e:
        log_error(f"File not found or cannot access file {dicom_file}: {e}")
        return [], 'Unknown SOP Class UID'
    except pydicom.errors.InvalidDicomError as e:
        log_error(f"Invalid DICOM file {dicom_file}: {e}")
        return [], 'Unknown SOP Class UID'
    except NotImplementedError as e:
        log_error(f"NotImplementedError while reading DICOM file {dicom_file}: {e}")
        return [], 'Unknown SOP Class UID'
    except Exception as e:
        log_error(f"Failed to read DICOM file {dicom_file}: {e}")
        return [], 'Unknown SOP Class UID'

    sop_class_uid = getattr(ds, 'SOPClassUID', 'Unknown SOP Class UID')

    header_info = []
    for elem in ds:
        if elem.tag.group != 0x7FE0:  # Exclude pixel data
            if elem.tag.group % 2 == 1:  # Private tag check
                continue
            tag_id = f"({elem.tag.group:04X},{elem.tag.element:04X})"
            try:
                value_str = str(elem.value)
            except Exception as e:
                value_str = f"Could not decode value: {e}"
            header_info.append({
                "T": tag_id,
                "A": elem.keyword,
                "V": value_str
            })
    return header_info, str(sop_class_uid)

# De-identify sensitive DICOM header information
def deidentify(header_info):
    deidentify_tags = {
        # Add tags that need to be de-identified
    }
    for item in header_info:
        if item["A"] in deidentify_tags:
            item["V"] = 'De-identified'
    return header_info

# Extract all DICOM headers with de-identification option
def extract_all_headers(dcm_files, deidentify_option=False):
    def extract_and_format(dicom_file):
        try:
            header, sop_class_uid = extract_dicom_header(dicom_file)
            if deidentify_option:
                header = deidentify(header)
            return {
                "File Name": dicom_file,
                "SOP Class UID": sop_class_uid,
                "Header": header
            }
        except Exception as e:
            log_error(f"Error extracting or formatting DICOM file {dicom_file}: {e}")
            return {
                "File Name": dicom_file,
                "SOP Class UID": 'Error',
                "Header": 'Error'
            }

    max_workers = multiprocessing.cpu_count()  # Dynamically set the max workers based on CPU cores

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        headers = list(executor.map(extract_and_format, dcm_files))
    return headers

# Write headers to CSV file
def write_headers_to_csv(headers, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as output:
            fieldnames = ["File Name", "SOP Class UID", "Header"]
            dict_writer = csv.DictWriter(output, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            dict_writer.writeheader()
            for header in headers:
                header['Header'] = str(header['Header'])  # Ensure header is string
                dict_writer.writerow(header)
    except IOError as e:
        log_error(f"Error writing to CSV file {output_file}: {e}")

# PyQt5 GUI class for the main window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DICOM Metadata Extractor')
        self.setGeometry(100, 100, 400, 250)

        layout = QVBoxLayout()

        self.button_select_directory = QPushButton('Select Directory', self)
        self.button_select_directory.clicked.connect(self.showDirectoryDialog)
        layout.addWidget(self.button_select_directory)

        self.button_select_output = QPushButton('Select Output File', self)
        self.button_select_output.clicked.connect(self.showFileDialog)
        layout.addWidget(self.button_select_output)

        self.button_extract_metadata = QPushButton('Extract Metadata', self)
        self.button_extract_metadata.clicked.connect(self.extract_metadata)
        layout.addWidget(self.button_extract_metadata)

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

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()

    def extract_metadata(self):
        if hasattr(self, 'directory') and hasattr(self, 'output_file'):
            self.progress_label.setText('Progress: 0%')
            self.progress_bar.setValue(0)

            try:
                dcm_files = find_dcm_files(self.directory)
                if not dcm_files:
                    self.show_error_message("No DICOM files found in the selected directory.")
                    return

                total_files = len(dcm_files)
                self.progress_bar.setMaximum(total_files)

                deidentify_option = True  # Adjust based on your logic or UI state

                all_headers = extract_all_headers(dcm_files, deidentify_option)
                write_headers_to_csv(all_headers, self.output_file)

                self.progress_bar.setValue(total_files)
                self.progress_label.setText(f'Completed processing {total_files} files.')
                print(f"Metadata extraction and saving to CSV completed at {self.output_file}")
            except Exception as e:
                self.show_error_message(f"An error occurred during extraction: {e}")
                log_error(f"An error occurred during extraction: {e}")
        else:
            self.show_error_message("Please select both Directory and Output File before extracting metadata.")

# Command-line argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description='DICOM Header Extractor')
    parser.add_argument('--directory', '-d', type=str, help='Directory to search for DICOM files')
    parser.add_argument('--output', '-o', type=str, help='Output CSV file name')
    parser.add_argument('--deidentify', '-di', action='store_true', help='Deidentify DICOM tags')

    args = parser.parse_args()
    return args

# Main function
if __name__ == "__main__":
    args = parse_arguments()

    if args.directory and args.output:
        directory_to_search = args.directory
        output_file = args.output
        deidentify_option = args.deidentify

        try:
            print(f"Searching for DICOM files in directory: {directory_to_search}")
            dcm_files = find_dcm_files(directory_to_search)
            print(f"Found {len(dcm_files)} DICOM files.")

            print("Extracting metadata...")
            all_headers = extract_all_headers(dcm_files, deidentify_option)

            print(f"Writing metadata to CSV file: {output_file}")
            write_headers_to_csv(all_headers, output_file)

            print(f"Metadata extraction and saving to CSV completed at {output_file}.")
        except Exception as e:
            log_error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")
    else:
        app = QApplication(sys.argv)
        ex = MainWindow()
        ex.show()
        sys.exit(app.exec_())
