
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
    return partNumber, revnum,all_data, 

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

from openpyxl import Workbook
from datetime import datetime
def NewPart(partNumber, partDescription, ClasssID, UnitPrice,RcvInspectionReq, ToolEdges2_C, ToolCat_c, ToolSubCat_c, ToolMfg_c,
            TDim_c, ToolDim_c, TRad_c, ToolRad_c, ToolAng_c, ToolFlute_c, TFluteLen_c, ToolFluteLen_c,
            TReach_c, ToolReach_c, TShank_c, ToolShank_c, ToolMtl_c, ToolCoat_c, ToolCoolant_c, tool_Notes_c,
            RevisionNum, RevShortDesc, RevDescription,drawNum, Approved, EffectiveDates, PartAuditChangeDescription,
            MinimumQty, MaximumQty, MinOrderQty, LeadTime, VendorNum):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H_%M_%S")
    EffectiveDate = current_datetime.strftime("%m/%d/%Y")


    # Create a new workbook and select the active sheet
    # *************************************************************************************************************************************************************************************************************
    Part = Workbook()
    Part_DMT = Part.active
    PartDMT = ["PartNum", "PartDescription", "ClassID", "UnitPrice","RcvInspectionReq", "ToolEdges2_C", "ToolCat_c",
               "ToolSubCat_c", "ToolMfg_c", "TDim_c", "ToolDim_c", "TRad_c", "ToolRad_c", "ToolAng_c",
               "ToolFlute_c", "TFluteLen_c", "ToolFluteLen_c", "TReach_c", "ToolReach_c", "TShank_c",
               "ToolShank_c", "ToolMtl_c", "ToolCoat_c", "ToolCoolant_c","ToolNotes_c", "Company", "IUM", "PUM", "TypeCode","NonStock","PricePerCode", "InternalPricePerCode", "CostMethod", "QtyBearing"]

    Part_DMT.append(PartDMT)
    
    for i, value in enumerate(partNumber):
        partlist = [value, partDescription[i], ClasssID[i], UnitPrice[i],RcvInspectionReq[i], ToolEdges2_C[i], ToolCat_c[i],
                    ToolSubCat_c[i], ToolMfg_c[i], TDim_c[i], ToolDim_c[i], TRad_c[i], ToolRad_c[i],
                    ToolAng_c[i], ToolFlute_c[i], TFluteLen_c[i], ToolFluteLen_c[i], TReach_c[i],
                    ToolReach_c[i], TShank_c[i], ToolShank_c[i], ToolMtl_c[i], ToolCoat_c[i],
                    ToolCoolant_c[i], tool_Notes_c[i], "JPMC","TOOL", "EA","P", "0", "E", "E", "S", "1"]
        Part_DMT.append(partlist)

    Part.save(fr"C:\FinalVsCodeProject\Part_DMT_{formatted_datetime}.xlsx")
    # *************************************************************************************************************************************************************************************************************
    
    revision = Workbook()
    Part_Rev = revision.active
    PartRev = ["PartNum", "RevisionNum", "RevShortDesc", "RevDescription","drawNum", "Approved", "EffectiveDate","AltMethod", "Company", "Plant", "PartAudit#ChangeDescription", "MinimumQty", "MaximumQty", "MinOrderQty", "LeadTime", "VendorNum"]

    Part_Rev.append(PartRev)        
    for i, value2 in enumerate(partNumber):
        revlist = [value2, RevisionNum[i], RevShortDesc[i], RevDescription[i],drawNum[i], Approved[i], EffectiveDate, "", "JPMC", "MfgSys", PartAuditChangeDescription[i]]
        Part_Rev.append(revlist)

    revision.save(fr"C:\FinalVsCodeProject\PartRev_DMT_{formatted_datetime}.xlsx")
    # *************************************************************************************************************************************************************************************************************
    plant = Workbook()
    Part_Plant = plant.active
    PartPlant = ["PartNum","MinimumQty", "MaximumQty", "MinOrderQty", "LeadTime", "VendorNum","PrimeWhse","ProcessMRP","SourceType", "NonStock","BuyerID","CostMethod","QtyBearing","AutoConsumeStock","RawMaterial","Company", "Plant", "PartAudit#ChangeDescription"]

    Part_Plant.append(PartPlant)        
    for i2, value2 in enumerate(partNumber):
        plantlist = [value2, MinimumQty[i2], MaximumQty[i2], MinOrderQty[i2], LeadTime[i2], VendorNum[i2],"JPMC", 0 ,1,"P", 0, "bpietran", "S", 1, 1, 1, "JPMC", "MfgSys",]
        Part_Plant.append(plantlist)

    plant.save(fr"C:\FinalVsCodeProject\PartPlant_DMT_{formatted_datetime}.xlsx")
    # *************************************************************************************************************************************************************************************************************
    Whse1 = Workbook()
    Part_Whse1 = Whse1.active
    PartPWhse1 = ["Company", "PartNum", "WarehouseCode", "DefaultWhse", "PrimeBinNum", "Plant"]

    Part_Whse1.append(PartPWhse1)        
    for i2, value2 in enumerate(partNumber):
        whse1list = ["JPMC", value2, "JPMC", 1, "JPMC", "MfgSys"]
        Part_Whse1.append(whse1list)

    Whse1.save(fr"C:\FinalVsCodeProject\PartWhse1_DMT_{formatted_datetime}.xlsx")
    # *************************************************************************************************************************************************************************************************************
    Whse2 = Workbook()
    Part_Whse2 = Whse2.active
    PartPWhse2 = ["Company", "PartNum", "WarehouseCode", "DefaultWhse", "PrimeBinNum", "Plant"]

    Part_Whse2.append(PartPWhse2)        
    for i2, value2 in enumerate(partNumber):
        whse2list = ["JPMC", value2, "TOOLCRIB", 1, "JPMC", "MfgSys"]
        Part_Whse2.append(whse2list)

    Whse2.save(fr"C:\FinalVsCodeProject\PartWhse2_DMT_{formatted_datetime}.xlsx")
    # *************************************************************************************************************************************************************************************************************
    BinInfo = Workbook()
    PartbinInfo = BinInfo.active
    binInfo = ["Company", "PartNum", "WarehouseCode", "PrimeBinNum", "Plant"]

    PartbinInfo.append(binInfo)        
    for i2, value2 in enumerate(partNumber):
        Bininfolist = ["JPMC", value2, "JPMC", "JPMC", "MfgSys"]
        PartbinInfo.append(Bininfolist)

    BinInfo.save(fr"C:\FinalVsCodeProject\PartBininfo_DMT_{formatted_datetime}.xlsx")
    
    return partNumber, partDescription

# Example usage with sample data
