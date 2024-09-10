# DICOM Header Extractor

This project extracts DICOM headers, de-identifies specific tags (optional), and saves the information to a CSV file. The repository provides two versions of the tool: one for terminal-based usage (command line) and another as a standalone executable (EXE) for environments without Python installed.

---

### 1. Terminal-Based DICOM Header Extractor
#### Files:
- **dicom-header-extractor_cmd.py**: The main script for extracting DICOM headers via the terminal.
- **dicom-header-extractor_cmd-guide.ipynb**: A Jupyter notebook guide explaining how to use the script in Python environments.

#### Usage Instructions:

1. **Install Dependencies**: 
   Ensure `pydicom` and other necessary packages are installed. You can install them using:
   ```bash
   pip install pydicom
   ```

2. **Command Line Usage**:
   The script requires two arguments: 
   - `--directory` or `-d`: The directory where DICOM files are located.
   - `--output` or `-o`: The name of the output CSV file where metadata will be saved.
   - Optionally, you can add the `--deidentify` or `-di` flag to de-identify sensitive metadata.
   
   Run the script:
   ```bash
   python dicom-header-extractor_cmd.py --directory '/path/to/directory/' --output '/path/to/output.csv' [--deidentify]
   ```


      This will search the provided directory for DICOM files, extract their metadata, and save it to a CSV file.

3. **Jupyter Notebook Guide**:
   You can find usage examples and details in `dicom-header-extractor_cmd-guide.ipynb`. This guide demonstrates how to run the script step-by-step in a notebook environment.

---

### 2. Standalone DICOM Header Extractor (EXE)
#### Files:
- **dicom-header-extractor_exe.zip**: The downloadable ZIP file containing the EXE version of the tool.
- **dicom-header-extractor_exe-source.py**: The Python source code for creating the standalone EXE.

#### Usage Instructions:

1. **Download and Extract**:
   - Download `dicom-header-extractor_exe.zip` from the repository.
   - Extract the contents to a directory of your choice.

2. **Run the Program**:
   - Open the extracted folder and run the EXE file in the `dist` folder.
   - The program opens a GUI where you can:
     - Select the directory containing DICOM files.
     - Specify the output CSV file.
     - Start the metadata extraction process.
   - A progress bar will show the status of the extraction.

3. **De-Identification**:
   The EXE version of the tool automatically de-identifies sensitive DICOM metadata during extraction. (9/10/2024: Not used)

4. **System Requirements**:
   - No Python installation is required to run the EXE file.
   - Ensure that your system supports running standalone applications built with PyQt5.

---

### Error Handling:
- All errors encountered during execution, such as permission issues or invalid DICOM formats, are logged in `error_log.txt` in the directory where the tool is executed.
  
## References
The DICOM tags selected for de-identification in this project are based on the following paper:
- Aryanto KYE, Oudkerk M, van Ooijen PMA. Free DICOM de-identification tools in clinical research: functioning and safety of patient privacy. Eur Radiol. 2015;25(12):3685-3695. doi:10.1007/s00330-015-3794-0

