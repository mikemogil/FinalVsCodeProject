
partNumber = ''
revnum = ''
def ExcelFiles(partNumber, partNew, rowsJob, rowsPart,revnum, non_Existing_ID):
    partNumber = partNumber
    revnum = revnum
    all_data = []
    jobscurrent = []
    startSeq = 1020
    rowsPart = [(partNumber, part[0], part[1], part[2], "***", revnum)for i, part in enumerate(rowsPart)]
  
    
    
    updated_part_new = [(partNumber,part[0], part[1], 0.01, "***", revnum) for i,part in enumerate(partNew)]
    if len(non_Existing_ID)>0:
        all_data = rowsPart + updated_part_new
    else:
        all_data = rowsPart

    import openpyxl
    prb = openpyxl.Workbook()
    partRevBom = prb.active
    column_headers = ['PartNum', 'RevisionNum','MtlSeq', 'MtlPartNum', 'QtyPer', 'RelatedOperation', 'UOMCode', 'Plant', 'ECOGroupID', 'Company' ]
    partRevBom.append(column_headers)
    for row in all_data:
        partRevBom.append([row[0], revnum, startSeq, row[1], row[3], 10, 'Tool', 'MFgSys', 'mdieckman', 'JPMC'])
        startSeq += 10

    prb.save(fr'J:\ERP-Business Intelligence\Bill of Materials (BOM)\BOM output\PRB,{partNumber},{revnum}.xlsx')
    for eachJob in rowsJob:
        startSeq = 1020
        for job in all_data:
            jobscurrent.append([eachJob['JobNum'], startSeq, job[1], job[3],'Tool', 0, 10, 'MFgSys', 'JPMC', job[2]])
            startSeq += 10

    jbm = openpyxl.Workbook()
    jobBom = jbm.active
    column_headers = ['JobNum', 'MtlSeq','PartNum', 'QtyPer','IUM','AssemblySeq', 'RelatedOperation', 'Plant', 'Company', 'Description' ]
    jobBom.append(column_headers)
    for row in jobscurrent:
        jobBom.append(row)
    jbm.save(fr'J:\ERP-Business Intelligence\Bill of Materials (BOM)\BOM output\JB,{partNumber},{revnum}.xlsx')    
    return partNumber, revnum

def pnrn():
    return partNumber, revnum