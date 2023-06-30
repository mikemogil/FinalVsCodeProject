from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import Engine   
from sqlalchemy import create_engine, MetaData, Table
from findfile import id_list_from_file, get_latest_file_path

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
engine = create_engine(url, echo=False)


def part(partNumber, dropdown):
    filepath = get_latest_file_path(partNumber, dropdown)
    idlist = id_list_from_file(filepath)

    finalList = [item for item in idlist]
    
        # Execute the query
    with engine.connect() as conn:
            queryPartNum = text("""
                SELECT p2.PartNum, p2.PartDescription, pm.QtyPer, pm.MtlSeq
                FROM dbo.Part p
                LEFT OUTER JOIN dbo.PartMtl pm ON p.PartNum = pm.PartNum
                LEFT OUTER JOIN dbo.Part p2 ON p2.PartNum = pm.MtlPartNum
                WHERE p.PartNum = :partNumber AND p2.partnum IN :idlist
                ORDER BY pm.MtlSeq
                """
            )

            queryJobNum = text("""
                SELECT JobHead.JobNum
                FROM EpicorLive11.Erp.JobHead JobHead, EpicorLive11.Erp.JobOpDtl JobOpDtl, EpicorLive11.Erp.JobOper JobOper, EpicorLive11.Erp.Resource Resource
                WHERE JobOper.Company = JobHead.Company
                AND JobHead.PartNum = :partNumber
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

            queryPartNum = queryPartNum.bindparams(partNumber = partNumber, idlist=finalList)
            queryJobNum = queryJobNum.bindparams(partNumber = partNumber)


            rowsPart = list(conn.execute(queryPartNum).fetchall())
            rowsJob = list(conn.execute(queryJobNum).fetchall())

            all_data = []

            existing_ids = [row[0] for row in rowsPart]
            non_existing_ids = [id for id in finalList if id not in existing_ids]
            print("Non-existing IDs:", non_existing_ids)
            print('\n\n')
            print("Existing IDs:", rowsPart)

            print("Current Jobs:", rowsJob)
            return rowsJob, rowsPart, filepath
            

    


