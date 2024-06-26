
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
  - No installation is required for end-users. Simply download the provided DICOM_Metadata_Extractor.exe file.

2. Execution:

  - Double-click DICOM_Metadata_Extractor.exe to launch the application.
  - The GUI will appear, allowing you to interact with the application.

3. Steps to Use:

  - Click on the Select Directory button to choose a folder containing DICOM files.
  - Click on the Select Output File button to specify the location and name of the CSV file where metadata will be saved.
  - Optionally, check the Deidentify DICOM Tags checkbox to anonymize sensitive DICOM tags during extraction.
  - Once both directory and output file are selected, click Extract Metadata to start the process.
  - The progress bar will show the progress of metadata extraction.
  - Upon completion, a message will indicate that the metadata has been saved to the CSV file.

### For macOS:

1. Prerequisites:

  - Ensure Python 3.x is installed on your macOS system.
  - Install PyQt5 using the following command:
    ```
    pip install PyQt5
    ```

2. Execution:

  - Open a terminal and navigate to the directory where main.py is located.
  - Run the command: python main.py to start the application.

3. Steps to Use:

  - The application GUI will launch.
  - Follow the same steps as described for Windows (steps 3 to 5 under Windows usage).

## Additional Notes

  - Configuration: Modify config.txt to adjust application settings such as default directories or other preferences.
  - Command-Line Usage: For advanced users, the application supports command-line arguments (--directory and --deidentify) to specify directory and deidentification options.
  - Troubleshooting: Ensure selected directories contain valid DICOM files and that the output file path is writable.

Thank you for using DICOM Metadata Extractor!
