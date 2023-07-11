from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import Engine   
from sqlalchemy import create_engine, MetaData, Table
from findfile import id_list_from_file, get_latest_file_path
import sqlalchemy as db
import excelBuilder
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

# def retrievefiles(partNumber):
#     return fileslist


def part(partNumber, revNum, idlist):
    revNum = revNum
    finalList = [item for item in idlist]
        # Execute the query
    print("Here is idlist:", idlist)
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
        SELECT DISTINCT JobHead.JobNum
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
        ORDER BY JobHead.JobNum
        """
            )

    queryPartNum = queryPartNum.bindparams(partNumber = partNumber, idlist=finalList, revNum = revNum)
    queryJobNum = queryJobNum.bindparams(partNumber = partNumber, revNum = revNum)


    rowsPart = list(conn.execute(queryPartNum).fetchall())
    rowsJob = list(conn.execute(queryJobNum).mappings().fetchall())
    
    print("Here is rows part:", rowsPart)

    existing_ids = [row[0] for row in rowsPart]
    non_existing_ids = [id for id in finalList if id not in existing_ids]

    # nonexistentids = db.text("""
    #     SELECT p2.PartDescription
    #     FROM dbo.Part p
    #     WHERE p.PartNum in :non_existing_ids
    #     """
    # )                    
    # nonexistentids = nonexistentids.bindparams(non_existing_ids = non_existing_ids)
    # nonExistingIDS = list(conn.execute(nonexistentids).fetchall())
    
    # print("Non-existing IDs:", non_existing_ids)
    # print('\n\n')
    # print("Existing IDs:", rowsPart)

    # print("Current Jobs:", rowsJob)
    partNew = ''
    if len(non_existing_ids) > 0:
        queryNew = db.text(("""
            SELECT p.PartNum, p.PartDescription
            FROM dbo.Part p
            WHERE p.partnum IN :non_existing_ids
        """
        ))
        partNew = queryNew.bindparams(non_existing_ids = non_existing_ids)
        partNew = list(conn.execute(partNew).fetchall())
        print(partNew, "Ne parts")
    else:
        partNew = []

    excelBuilder.ExcelFiles(partNumber, partNew, rowsJob, rowsPart,revNum, non_existing_ids)
      
    return rowsJob, rowsPart, filepath, non_existing_ids
            
def getDescription(mtlPartNum):
    partDesc = db.text("""
        SELECT p.PartDescription
        FROM dbo.Part p
        WHERE p.PartNum = :mtlPartNum
        """
    )
    partDesc = partDesc.bindparams(mtlPartNum = mtlPartNum)
    description = conn.execute(partDesc).fetchone()
    if len(description) > 1:
        description = description[0]
    # q: my description onlly return a single value, how do I get the value out of the tuple?
    # q: how do I get the value out of the tuple?


    return description

    


