import glob
import re
import os
import xml
import xml.etree.ElementTree as ET
from inspect import getmembers, isclass,isfunction


# # *********************************************************************

# #Getting the correct filepath
# files = glob.glob(r"X:\PROGRAMMING\CUSTOMER\CROSSROADS\MPJ Plate\260224-5V10D18_REVC\Current\*")
# parent_directory = "X:\PROGRAMMING\CUSTOMER"
# partnum = 'DRW-02446-01'
# filePath = glob.glob(fr"{parent_directory}\**\*{partnum}*.tls", recursive=True)
# print("****************************************************************\n\n")
# print(filePath)
# print("****************************************************************\n\n")
# if filePath:
#     latest_file = max(filePath, key=os.path.getmtime)
#     print("Latest modified file:", latest_file)
# else:
#     print("No files matching the pattern found.")

# # *********************************************************************


tree = ET.parse(r'X:\PROGRAMMING\CUSTOMER\SKELETAL DYNAMICS\RADIAL HEAD PLATE, EXTENDED\DRW-02446-01_revRAB\VERICUT\RD_5-9-23_DRW-02446-01_revRAB2-Toolpath Group-1.tls  ')

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
        print("ID value:", id_value)
        idlist.append(id_value)


#  ****************************************************************************************  
# Using Sqlalchemy to extract data
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import Engine   
from sqlalchemy import create_engine, MetaData, Table


E10_conn_args = {
    'drivername': 'mssql+pymssql',
    'username': 'production',
    'password': 'production',
    'host': 'phl-db-01',
    'port': '1433',
    'database': 'EpicorLive11'
}

url = URL.create(**E10_conn_args)

engine = create_engine(url, echo=False )

def get_db():
    with engine.connect() as conn:
        yield conn



finalList = [item for item in idlist]



# Execute the query
with engine.connect() as conn:
    queryPartNum = text("""
        SELECT p2.PartNum, p2.PartDescription, pm.QtyPer, pm.MtlSeq
        FROM dbo.Part p
        LEFT OUTER JOIN dbo.PartMtl pm ON p.PartNum = pm.PartNum
        LEFT OUTER JOIN dbo.Part p2 ON p2.PartNum = pm.MtlPartNum
        WHERE p.PartNum = 'DRW-02446-01' AND p2.partnum IN :idlist
        ORDER BY pm.MtlSeq
        """
    )

    queryJobNum = text("""
        SELECT JobHead.JobNum
        FROM EpicorLive11.Erp.JobHead JobHead, EpicorLive11.Erp.JobOpDtl JobOpDtl, EpicorLive11.Erp.JobOper JobOper, EpicorLive11.Erp.Resource Resource
        WHERE JobOper.Company = JobHead.Company
        AND JobHead.PartNum = 'DRW-02446-01'
        AND JobOper.JobNum = JobHead.JobNum
        AND JobOpDtl.AssemblySeq = JobOper.AssemblySeq
        AND JobOpDtl.Company = JobHead.Company
        AND JobOpDtl.Company = JobOper.Company
        AND JobOpDtl.JobNum = JobHead.JobNum
        AND JobOpDtl.JobNum = JobOper.JobNum 
        AND JobOpDtl.OprSeq = JobOper.OprSeq
        AND Resource.Company = JobHead.Company
        AND Resource.Company = JobOpDtl.Company
        AND Resource.Company = JobOper.Company
        AND Resource.ResourceID = JobOpDtl.ResourceID
        AND ((JobHead.Company='JPMC') AND (JobOper.OpComplete=0) AND (JobOper.OpCode In ('SWISS','CNC')))
        ORDER BY JobHead.PartNum
        """
    )
    

    
   
    queryPartNum = queryPartNum.bindparams(idlist = finalList)
    
    rowsPart = list(conn.execute(queryPartNum).fetchall())
    rowsJob = list(conn.execute(queryJobNum).fetchall())

    all_data = []
     
    existing_ids = [row[0] for row in rowsPart]
    non_existing_ids = [id for id in finalList if id not in existing_ids]
    print("Non-existing IDs:", non_existing_ids)
    print('\n\n')
    print("Existing IDs:", rowsPart)

    print("Current Jobs:", rowsJob)

    


from flask import Flask, request, render_template
import pandas as pd
app = Flask(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    # Read Excel data using pandas
    df = pd.read_excel('C:\FinalVsCodeProject\output.xlsx')
    
    # Convert DataFrame to a list of lists for Handsontable
    data = df.values.tolist()
    
    # Get column headers
    headers = df.columns.tolist()
    
    return render_template('main.html', data=data, headers=headers)

if __name__ == '__main__':
    app.run(debug=True)

