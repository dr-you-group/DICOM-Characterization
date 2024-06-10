import csv

def save_to_csv(header_info_list, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as output:
        fieldnames = ["File Name", "SOP Class UID", "Tag", "Attribute Name", "Value"]
        dict_writer = csv.DictWriter(output, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        dict_writer.writeheader()
        for header_info in header_info_list:
            for item in header_info["Header"]:
                row = {
                    "File Name": header_info["File Name"],
                    "SOP Class UID": header_info["SOP Class UID"],
                    "Tag": item["Tag"],
                    "Attribute Name": item["Attribute Name"],
                    "Value": item["Value"]
                }
                dict_writer.writerow(row)