import glob
import os
import xml.etree.ElementTree as ET
# ***********************************************************************************************************************************  

def get_latest_file_path(partnum, dropdown):
    parent_directory = r"\\192.168.10.22\Robo FTP\PROGRAMMING\CUSTOMER"
    filePath = glob.glob(fr"{parent_directory}\{dropdown}\**\*{partnum}*.tls", recursive=True)
    print(dropdown)
    if filePath:
        latest_file = max(filePath, key=os.path.getmtime)
        print(latest_file)
    else:
        print("No files matching the pattern found.")
        latest_file = 0


    return filePath, latest_file
# ***********************************************************************************************************************************  
def id_list_from_file(files):
 

    idlist = []

    for file in files:
        print(file)
        tree = ET.parse(file)
        root = tree.getroot()
        parent_elements = root.findall(".//Tools/Tool/Cutter")
        for parent_element in parent_elements:
            sor_element = parent_element.find("SOR")
            if sor_element is not None:
                id_value = sor_element.get("ID")
                idlist.append(id_value)
    return idlist
# ***********************************************************************************************************************************  


