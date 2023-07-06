
partNumber = ''
revnum = ''
def ExcelFiles(partNumber, partNew, rowsJob, rowsPart,revnum):
    partNumber = partNumber
    revnum = revnum
    all_data = []
    jobscurrent = []
    start_sequence_number = 1020
    increment = 10
    rowsPart = [(partNumber, part[0], part[1], part[2], start_sequence_number + i * increment, revnum)for i, part in enumerate(rowsPart)]
    startSeq = rowsPart[-1]
    updated_part_new = [(partNumber,part[0], part[1], 0.01, startSeq[4] + i * increment, revnum) for i,part in enumerate(partNew)]

    all_data = rowsPart + updated_part_new
    print (rowsPart + updated_part_new)
    import openpyxl
    prb = openpyxl.Workbook()
    partRevBom = prb.active
    column_headers = ['PartNum', 'RevisionNum','MtlSeq', 'MtlPartNum', 'QtyPer', 'RelatedOperation', 'UOMCode', 'Plant', 'ECOGroupID', 'Company' ]
    partRevBom.append(column_headers)
    for row in all_data:
        partRevBom.append([row[0], revnum, row[4], row[1], row[3], 10, 'Tool', 'MFgSys', 'mdieckman', 'JPMC'])
    prb.save(f'PRB,{partNumber},{revnum}.xlsx')

    for eachJob in rowsJob:
        
        for job in all_data:
            jobscurrent.append([eachJob['JobNum'], job[4], job[1], job[3],'Tool', 0, 10, 'MFgSys', 'JPMC', job[2]])
    jbm = openpyxl.Workbook()
    jobBom = jbm.active
    column_headers = ['JobNum', 'MtlSeq','PartNum', 'QtyPer','IUM','AssemblySeq', 'RelatedOperation', 'Plant', 'Company', 'Description' ]
    jobBom.append(column_headers)
    for row in jobscurrent:
        jobBom.append(row)
    jbm.save(f'JB,{partNumber},{revnum}.xlsx')    
    return partNumber, revnum

def pnrn():
    return partNumber, revnum