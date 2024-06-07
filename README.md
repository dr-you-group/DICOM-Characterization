# DICOM Header Extractor

This project extracts DICOM headers, de-identifies specific tags, and saves the information to a CSV file.

## Requirements

To run this project, you need the following libraries:
- Pydicom

If Pydicom is not installed on your system, you can install it using the following command:
    ```
    pip install pydicom
    ```


## Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/dr-you-group/dicom-header-extractor.git
    cd dicom-header-extractor
    ```

2. Set the directory to search for DICOM files in `config.txt`.

3. Run the script:
    ```bash
    python main.py
    ```

The output CSV file will be generated in the same directory.
