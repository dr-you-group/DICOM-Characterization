import pydicom

def extract_dicom_header(dicom_file):
    ds = pydicom.dcmread(dicom_file)
    if ds.SOPClassUID:
        sop_class_uid = ds[(0x0008, 0x0016)].value
    else:
        sop_class_uid = 'Unknown SOP Class UID'
    header_info = []
    for elem in ds:
        if elem.tag.group != 0x7FE0:  # Exclude pixel data
            tag_id = f"({elem.tag.group:04X},{elem.tag.element:04X})"
            header_info.append({
                "Tag": tag_id,
                "Attribute Name": elem.keyword,
                "Value": str(elem.value)
            })
    return header_info, str(sop_class_uid)