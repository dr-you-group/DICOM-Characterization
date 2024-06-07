from find_dcm_files import find_dcm_files
from extract_dicom_header import extract_dicom_header
from deidentify import deidentify
from save_to_csv import save_to_csv

def load_config(config_file='config.txt'):
    config = {}
    with open(config_file, 'r') as file:
        for line in file:
            name, value = line.strip().split('=')
            config[name] = value
    return config

if __name__ == "__main__":
    config = load_config()
    directory_to_search = config.get('directory_to_search', '.')
    
    dcm_files = find_dcm_files(directory_to_search)
    
    all_headers = []
    for dicom_file in dcm_files:
        header = extract_dicom_header(dicom_file)
        header = deidentify(header)
        all_headers.append({
            "File Name": dicom_file,
            "Header": header
        })
    
    save_to_csv(all_headers, 'output.csv')
