import glob
import os
import xml.etree.ElementTree as ET
# ***********************************************************************************************************************************  

def get_latest_file_path(partnum):
    parent_directory = r"X:\PROGRAMMING\CUSTOMER"
    filePath = glob.glob(fr"{parent_directory}\**\*{partnum}*.tls", recursive=True)
    
    if filePath:
        latest_file = max(filePath, key=os.path.getmtime)
        id_list_from_file(latest_file)
        return latest_file
    else:
        print("No files matching the pattern found.")
        return None
# ***********************************************************************************************************************************  

def id_list_from_file(latest_file):
    tree = ET.parse(latest_file)

    root = tree.getroot()
    parent_elements = root.findall(".//Tools/Tool/Cutter")
    idlist = []
# Iterate over the parent elements
    for parent_element in parent_elements:
    # Find the nested element "SOR" using its tag
        sor_element = parent_element.find("SOR")
    
    # Check if the "SOR" element exists within the parent element
        if sor_element is not None:
        # Access the value of the attribute "ID"
            id_value = sor_element.get("ID")
        
        # Print the attribute value
            
            idlist.append(id_value)
    return idlist
# ***********************************************************************************************************************************  


