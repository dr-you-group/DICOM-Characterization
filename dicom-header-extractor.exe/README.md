# DICOM Metadata Extractor README

This README provides instructions on how to use the DICOM Metadata Extractor application on both macOS and Windows platforms.

## Overview

DICOM Metadata Extractor is a graphical user interface (GUI) application developed using PyQt5 and Python. It allows users to extract metadata from DICOM files and save it to a CSV file. The application supports both Windows and macOS environments.

## Features

- Select Directory: Choose a directory where DICOM files are located.
- Select Output File: Specify the location and name of the CSV file for saving metadata.
- Deidentify DICOM Tags: An optional feature to anonymize sensitive DICOM tags.
- Progress Bar: Displays the progress of metadata extraction.
- Completion Message: Notifies when the process of metadata extraction and CSV saving is completed.

## Usage Instructions

### For Windows:

1. Installation:
   - Download the Windows installer [here](https://drive.google.com/file/d/1_WwMhjJL4Wje2_fNypDZK0kUE_3KFiMl/view?usp=sharing).
   - Extract the downloaded ZIP file.
   - Inside the extracted folder, run `dicom-header-extractor.exe` to launch the application.

2. Steps to Use:
   - Click on the Select Directory button to choose a folder containing DICOM files.
   - Click on the Select Output File button to specify the location and name of the CSV file where metadata will be saved.
   - Optionally, check the Deidentify DICOM Tags checkbox to anonymize sensitive DICOM tags during extraction.
   - Once both directory and output file are selected, click Extract Metadata to start the process.
   - The progress bar will show the progress of metadata extraction.
   - Upon completion, a message will indicate that the metadata has been saved to the CSV file.

### For macOS:

1. Installation:
   - Download the macOS installer [here](https://drive.google.com/file/d/1csmpAYqmiIF60swIJA4TUmD_gKxFd1Se/view?usp=drive_link).
   - Extract the downloaded ZIP file.
   - Inside the extracted folder, run `dicom-header-extractor.app` to install the application.

2. Steps to Use:
   - Open the Applications folder and find DICOM Metadata Extractor.
   - Double-click `main.app` to launch the application.
   - Follow the same steps as described for Windows (steps 2 to 5 under Windows usage).

## Additional Notes

- Configuration: Modify config.txt to adjust application settings such as default directories or other preferences.
- Command-Line Usage: For advanced users, the application supports command-line arguments (--directory and --deidentify) to specify directory and deidentification options.
- Troubleshooting: Ensure selected directories contain valid DICOM files and that the output file path is writable.

Thank you for using DICOM Metadata Extractor!
