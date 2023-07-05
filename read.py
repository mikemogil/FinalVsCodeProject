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
# partnum = '2*7*8*3*1*0'
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


tree = ET.parse(r"X:\PROGRAMMING\CUSTOMER\SEA SPINE\PROTEUS PROXIMAL BODY\ET1-302807-10_REVF\Current\VERICUT\SMS_2-7-23_ET1-302807-10-ET1-302807-10 REVF Op1 .tls")

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
import sqlalchemy as db
from openpyxl import Workbook


E10_conn_args = {
    'drivername': 'mssql+pymssql',
    'username': 'production',
    'password': 'production',
    'host': 'phl-db-01',
    'port': '1433',
    'database': 'EpicorLive11'
}

url = URL.create(**E10_conn_args)

engine = db.create_engine(url, echo=False )

connection = engine.connect()




finalList = [item for item in idlist]



# Execute the query

queryPart = db.text("""
    SELECT p2.PartNum, p2.PartDescription, pm.QtyPer 
    FROM dbo.Part p
    LEFT OUTER JOIN dbo.PartMtl pm ON p.PartNum = pm.PartNum
    LEFT OUTER JOIN dbo.Part p2 ON p2.PartNum = pm.MtlPartNum
    WHERE p.PartNum = 'ET1-302807-10'And pm.RevisionNum = 'F' AND p2.partnum IN :idlist
    ORDER BY pm.MtlSeq
    """
)
# # SELECT p2.PartNum, p2.PartDescription, jh.RevisionNum 
#     FROM dbo.Part p
#     LEFT OUTER JOIN dbo.PartMtl pm ON p.PartNum = pm.PartNum
#     LEFT OUTER JOIN dbo.Part p2 ON p2.PartNum = pm.MtlPartNum
#     LEFT OUTER JOIN dbo.JobHead jh On p.PartNum = jh.PartNum 
#     WHERE p.PartNum = 'ET1-302807-10' AND jh.RevisionNum = 'F' And p2.partnum IN ('T80836', 'T80868', '902531-C3', '05-0047', 'VQ4SVBR0150', '36210-C3', '36210-C3', 'T70026', '26340-C3', '53631-C6', '24662-C3', '24662-C3', '74331-C3', '01012', '65108-C3', '26340-C3', '33420-C3', '28145-C3', '28145-C3', '13037', '71030-C3', '67839-C3', '997962-C3')
#     ORDER BY pm.MtlSeq

queryJobNum = db.text("""
    SELECT JobHead.JobNum
    FROM EpicorLive11.Erp.JobHead JobHead, EpicorLive11.Erp.JobOpDtl JobOpDtl, EpicorLive11.Erp.JobOper JobOper, EpicorLive11.Erp.Resource Resource
    WHERE JobOper.Company = JobHead.Company
    AND JobHead.PartNum = 'ET1-302807-10'
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
    
print(idlist)
    
   
queryPart = queryPart.bindparams(idlist = finalList)

    
rowsPart = list(connection.execute(queryPart).fetchall())
rowsJob = list(connection.execute(queryJobNum).mappings().fetchall())
# if len(rowsJob == 1): rowsJob = rowsJob[0]

all_data = []
for job in rowsJob:
    print(job['JobNum'])  

existing_ids = [row[0] for row in rowsPart]
non_existing_ids = [id for id in finalList if id not in existing_ids]
print("Non-existing IDs:", non_existing_ids)
print('\n\n')
print("Existing Id:", existing_ids)


non_existing_ids = [item for item in non_existing_ids]

queryNew = db.text(("""
    SELECT p.PartNum, p.PartDescription
    FROM dbo.Part p
    WHERE p.partnum IN :non_existing_ids
    """
))

partNew = queryNew.bindparams(non_existing_ids = non_existing_ids)
partNew = list(connection.execute(partNew).fetchall())
partnewList = partNew
jobscurrent = []
start_sequence_number = 1020
increment = 10
revNum = 'B'
rowsPart = [('ET1-302807-10', part[0], part[1], part[2], start_sequence_number + i * increment, revNum)for i, part in enumerate(rowsPart)]
startSeq = rowsPart[-1]
updated_part_new = [('ET1-302807-10',part[0], part[1], 0.01, startSeq[4] + i * increment, revNum) for i,part in enumerate(partNew)]

all_data = rowsPart + updated_part_new
print (rowsPart + updated_part_new)
import openpyxl
prb = openpyxl.Workbook()
partRevBom = prb.active
column_headers = ['PartNum', 'RevisionNum','MtlSeq', 'MtlPartNum', 'QtyPer', 'RelatedOperation', 'UOMCode', 'Plant', 'ECOGroupID', 'Company' ]
partRevBom.append(column_headers)
for row in all_data:
    partRevBom.append([row[0], row[5], row[4], row[1], row[3], 10, 'Tool', 'MFgSys', 'mdieckman', 'JPMC'])
prb.save('data_sheet.xlsx')

for eachJob in rowsJob:
    
    for job in all_data:
        jobscurrent.append([eachJob['JobNum'], job[4], job[1], job[3],'Tool', 0, 10, 'MFgSys', 'JPMC', job[2]])
jbm = openpyxl.Workbook()
jobBom = jbm.active
column_headers = ['JobNum', 'MtlSeq','PartNum', 'QtyPer','IUM','AssemblySeq', 'RelatedOperation', 'Plant', 'Company', 'Description' ]
jobBom.append(column_headers)
for row in jobscurrent:
    jobBom.append(row)
jbm.save('data_sheet2.xlsx')
