from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import Engine   
from sqlalchemy import create_engine, MetaData, Table
from findfile import id_list_from_file, get_latest_file_path
import sqlalchemy as db

# ********************************************************

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image

E10_conn_args = {
        'drivername': 'mssql+pymssql',
        'username': 'production',
        'password': 'production',
        'host': 'phl-db-01',
        'port': '1433',
        'database': 'EpicorLive11'
}

url = URL.create(**E10_conn_args)


filepath = ''
engine = db.create_engine(url, echo=False)
conn = engine.connect()


def part(partNumber, revNum, dropdown):
    filepath = get_latest_file_path(partNumber, dropdown)
    idlist = id_list_from_file(filepath)
    revNum = revNum
    finalList = [item for item in idlist]
    
        # Execute the query

    queryPartNum = db.text("""
        SELECT p2.PartNum, p2.PartDescription, pm.QtyPer
        FROM dbo.Part p
        LEFT OUTER JOIN dbo.PartMtl pm ON p.PartNum = pm.PartNum
        LEFT OUTER JOIN dbo.Part p2 ON p2.PartNum = pm.MtlPartNum
        WHERE p.PartNum = :partNumber AND p2.partnum IN :idlist AND pm.RevisionNum = :revNum
        ORDER BY pm.MtlSeq
        """
    )

    queryJobNum = db.text("""
        SELECT JobHead.JobNum
        FROM EpicorLive11.Erp.JobHead JobHead, EpicorLive11.Erp.JobOpDtl JobOpDtl, EpicorLive11.Erp.JobOper JobOper, EpicorLive11.Erp.Resource Resource
        WHERE JobOper.Company = JobHead.Company
        AND JobHead.PartNum = :partNumber 
        And JobHead.RevisionNum = :revNum
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

    queryPartNum = queryPartNum.bindparams(partNumber = partNumber, idlist=finalList, revNum = revNum)
    queryJobNum = queryJobNum.bindparams(partNumber = partNumber, revNum = revNum)


    rowsPart = list(conn.execute(queryPartNum).fetchall())
    rowsJob = list(conn.execute(queryJobNum).mappings().fetchall())

    all_data = []

    existing_ids = [row[0] for row in rowsPart]
    non_existing_ids = [id for id in finalList if id not in existing_ids]
    print("Non-existing IDs:", non_existing_ids)
    print('\n\n')
    print("Existing IDs:", rowsPart)

    print("Current Jobs:", rowsJob)
    queryNew = db.text(("""
        SELECT p.PartNum, p.PartDescription
        FROM dbo.Part p
        WHERE p.partnum IN :non_existing_ids
    """
    ))
    partNew = queryNew.bindparams(non_existing_ids = non_existing_ids)

    partNew = list(conn.execute(partNew).fetchall())

    # *************************************************************************
    jobscurrent = []
    start_sequence_number = 1020
    increment = 10
    revNum = 'B'
    rowsPart = [(partNumber, part[0], part[1], part[2], start_sequence_number + i * increment, revNum)for i, part in enumerate(rowsPart)]
    startSeq = rowsPart[-1]
    updated_part_new = [(partNumber,part[0], part[1], 0.01, startSeq[4] + i * increment, revNum) for i,part in enumerate(partNew)]

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
    return rowsJob, rowsPart, filepath
            

    


