import os

def find_dcm_files(directory):
    dcm_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.dcm'):
                dcm_files.append(os.path.join(root, file))
    return dcm_files