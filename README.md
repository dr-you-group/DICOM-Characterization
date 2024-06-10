# DICOM Header Extractor

This project extracts DICOM headers, de-identifies specific tags (optional), and saves the information to a CSV file.

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

2. Set the directory to search for DICOM files and the de-identification option in `config.txt`.


    Example `config.txt`:
    ```
    directory_to_search=/path/to/your/directory
    deidentify=False
    ```

3. Run the script:
    ```bash
    python main.py
    ```

The output CSV file will be generated in the same directory.

## Output
The final output is a CSV file that contains the following columns for each DICOM file:
- File Name
- SOP Class UID
- Tag
- Attribute Name
- Value


## Guide

For a step-by-step guide, please refer to the Jupyter Notebook file `DICOM_Header_Extractor_Guide.ipynb`.


## References

The DICOM tags selected for de-identification in this project are based on the following paper:
- Aryanto KYE, Oudkerk M, van Ooijen PMA. Free DICOM de-identification tools in clinical research: functioning and safety of patient privacy. Eur Radiol. 2015;25(12):3685-3695. doi:10.1007/s00330-015-3794-0
