
import openpyxl

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
    return partNumber, revnum,all_data

def secondexcelBuilder(workbook_pathPRB, workbook_pathJB, edited_dataPRB, edited_dataJB, newPartNum, newQtyPer, operatingjobs, partNumber, revnum, dataLength):
    workbookPRB = openpyxl.load_workbook(workbook_pathPRB)
    workbookJB = openpyxl.load_workbook(workbook_pathJB)
    sheetPRB = workbookPRB.active
    sheetJB = workbookJB.active
    sheetPRB.delete_rows(2, sheetPRB.max_row)
    sheetJB.delete_rows(2, sheetJB.max_row)
    for i, newparts in enumerate(newPartNum):
        edited_dataPRB.append(partNumber)
        edited_dataPRB.append(revnum)
        edited_dataPRB.append("mtl")
        edited_dataPRB.append(newparts)
        edited_dataPRB.append(newQtyPer[i])
        edited_dataPRB.append("10")
        edited_dataPRB.append("Tool")
        edited_dataPRB.append("MFgSys")
        edited_dataPRB.append("Mdieckman")
        edited_dataPRB.append("JPMC")

    seqnumber = len(dataLength) * 10 + 1020
    print(operatingjobs)
    for jobnums in operatingjobs:
        for i, newparts in enumerate(newPartNum):
            edited_dataJB.append(jobnums)
            edited_dataJB.append(seqnumber)
            seqnumber += 10
            edited_dataJB.append(newparts)
            edited_dataJB.append(newQtyPer[i])
            edited_dataJB.append("Tool")
            edited_dataJB.append("0")
            edited_dataJB.append("10")
            edited_dataJB.append("MFgSys")
            edited_dataJB.append("JPMC")
            edited_dataJB.append("desc")
            print(jobnums)
        seqnumber = len(dataLength) * 10 + 1020
    return edited_dataJB, edited_dataPRB, sheetPRB, sheetJB, workbookPRB, workbookJB