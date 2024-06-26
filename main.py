import argparse
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

def parse_arguments():
    parser = argparse.ArgumentParser(description='DICOM Header Extractor')
    parser.add_argument('--directory', '-d', type=str, default='.', help='Directory to search for DICOM files')
    parser.add_argument('--deidentify', '-di', action='store_true', help='Deidentify DICOM tags')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    directory_to_search = args.directory
    deidentify_option = args.deidentify
    
    dcm_files = find_dcm_files(directory_to_search)
    
    all_headers = []
    for dicom_file in dcm_files:
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
    
    save_to_csv(all_headers, 'output.csv')
