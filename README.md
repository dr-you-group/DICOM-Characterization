# DICOM Header Extractor

This project extracts DICOM headers, de-identifies specific tags, and saves the information to a CSV file.

## Directory Structure

dicom-header-extractor/
│
├── README.md
├── config.txt
├── find_dcm_files.py
├── extract_dicom_header.py
├── deidentify.py
├── save_to_csv.py
└── main.py

## Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/dicom-header-extractor.git
    cd dicom-header-extractor
    ```

2. Set the directory to search for DICOM files in `config.txt`.

3. Run the script:
    ```bash
    python main.py
    ```

The output CSV file will be generated in the same directory.
