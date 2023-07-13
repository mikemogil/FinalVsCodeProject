from flask import Flask, render_template, request, redirect, url_for
import os
import json
from data_file import part, getDescription
import openpyxl
from findfile import get_latest_file_path, id_list_from_file
import smtplib
from excelBuilder import secondexcelBuilder
from data_file import getJobNum

directory_path = r"X:\PROGRAMMING\CUSTOMER"
dropdown = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]

app = Flask(__name__)
# data_file.engine

@app.route('/')
def form():
    return render_template('main.html', dropdown = dropdown)




@app.route('/submit-form', methods=['POST'])
def submit_form():
    if 'selected_files' in request.form:
        part_number = request.form.get('part_number')
     
        selected_files = request.form.getlist('selected_files')
        # full_file_path = request.form.getlist('full_file_path')
        revision_number = request.form.get('revision_number')
        dropdown_value = request.form.get('dropdown_value')
        partnum_values_ID = id_list_from_file(selected_files)

        return redirect(url_for('success', part_number = part_number, revision_number = revision_number, selected_files = partnum_values_ID,  dropdown_value = dropdown_value))
    else:
        
        part_number = request.form['partNumber']
        part_number = part_number.replace(" ", "")
        revision_number = request.form['revisionNumber']
        dropdown_value = request.form['dropdown_value']
        filepaths = get_latest_file_path(part_number,dropdown_value)
        print(filepaths[1])
        return render_template('files.html', part_number=part_number, revision_number=revision_number, dropdown_value=dropdown_value, selected_files = filepaths[0], latest_file = filepaths[1])
    


@app.route('/success', methods=['GET', 'POST'])
def success():

    
    if request.method == 'POST':
        # Get the edited data from the form
        selected_files = request.form.get('selected_files')
        # selected_files = eval(selected_files)
        part_number = request.form.get('part_number')
        revision_number = request.form.get('revision_number')
        edited_dataPRB = request.form.getlist('edited_dataPRB')
        edited_dataJB = request.form.getlist('edited_dataJB')
        newPartNum = request.form.getlist('partNum')
        newQtyPer = request.form.getlist('qtyPer')
        dataLength = request.form.getlist('jobs')
        jobs = getJobNum(part_number, revision_number)
        for job in jobs:
             print(job)
        # part(part_number, revision_number, selected_files)
        workbook_pathPRB = fr'J:\ERP-Business Intelligence\Bill of Materials (BOM)\BOM output\PRB,{part_number},{revision_number}.xlsx'
        workbook_pathJB = fr'J:\ERP-Business Intelligence\Bill of Materials (BOM)\BOM output\JB,{part_number},{revision_number}.xlsx' 
        

        secondBuilder = secondexcelBuilder(workbook_pathPRB, workbook_pathJB, edited_dataPRB, edited_dataJB, newPartNum, newQtyPer, jobs, part_number, revision_number, dataLength)
        seqPRB  = 1020
        for i, value in enumerate(secondBuilder[1]):
            row_number = i // secondBuilder[2].max_column + 2  # Add 2 to skip the header row
            col_number = i % secondBuilder[3].max_column + 1
            if col_number == 1:
                 cellvalueP = str(part_number)
            elif col_number == 2:
                 cellvalueP = revision_number
            elif col_number == 3:
                cellvalueP = str(seqPRB) # Convert mtlSeqPRBss to an integer, add 10, and then convert back to a string
                seqPRB = seqPRB + 10
            elif col_number == 4:
                 cellvalueP = value
            elif col_number == 5:
                 cellvalueP = value
            elif col_number == 6:
                 cellvalueP = '10'
            elif col_number == 7:
                 cellvalueP = 'Tool'
            elif col_number == 8:
                 cellvalueP = 'MFgSys'
            elif col_number == 9:
                 cellvalueP = 'mdieckman'
            elif col_number == 10:
                 cellvalueP = "JPMC"
            else:
                 cellvalueP = value
            
            secondBuilder[2].cell(row=row_number, column=col_number).value = cellvalueP

            

        seqJB = 1020
        for i, value in enumerate(secondBuilder[0]):
            row_number = i // secondBuilder[3].max_column + 2  # Add 2 to skip the header row
            col_number = i % secondBuilder[3].max_column + 1
            if col_number == 2:
                cellvalueJ = str(seqJB) # Convert mtlSeqPRBss to an integer, add 10, and then convert back to a string
                seqJB = seqJB + 10 
            elif col_number == 5:
                 cellvalueJ = 'Tool'
            elif col_number == 6:
                 cellvalueJ = '0'
            elif col_number == 7:
                 cellvalueJ = '10'
            elif col_number == 8:
                 cellvalueJ = 'MFgSys'
            elif col_number == 9:
                 cellvalueJ = 'JPMC'
            elif col_number == 10:
                 
               cellvalueJ = str(getDescription(secondBuilder[3].cell(row=row_number, column=3).value))[2:-3] 
               print(cellvalueJ)
               
            else:
                cellvalueJ = value
            secondBuilder[3].cell(row=row_number, column=col_number).value = cellvalueJ

        # Save the changes back to the Excel file
        secondBuilder[4].save(workbook_pathPRB)
        secondBuilder[5].save(workbook_pathJB)

        # Redirect to the success page
        

        return render_template('finished.html')
    else:
        # Get the initial data from the Excel sheet

        selected_files = request.args.getlist('selected_files')
        dropdown = request.args.get('dropdown_value')
        part_number = request.args.get('part_number')
        revision_number = request.args.get('revision_number')
        

        
        partinfo = part(part_number, revision_number, selected_files)

        workbook_pathPRB = fr'J:\ERP-Business Intelligence\Bill of Materials (BOM)\BOM output\PRB,{part_number},{revision_number}.xlsx'
        workbook_pathJB = fr'J:\ERP-Business Intelligence\Bill of Materials (BOM)\BOM output\JB,{part_number},{revision_number}.xlsx' 

        workbookPRB = openpyxl.load_workbook(workbook_pathPRB)
        workbookJB = openpyxl.load_workbook(workbook_pathJB)
        sheetPRB = workbookPRB.active
        sheetJB = workbookJB.active

        headersPRB = [cell.value for cell in sheetPRB[1]]
        headersJB = [cell.value for cell in sheetJB[1]]
        dataPRB = []
        dataJB = []
        
            
        for rowPRB in sheetPRB.iter_rows(min_row=2, values_only=True):
            dataPRB.append(rowPRB)

        for rowJB in sheetJB.iter_rows(min_row=2, values_only=True):
                    dataJB.append(rowJB)

        return render_template('excel.html', part_number=part_number, revision_number=revision_number,
                                headersPRB=headersPRB, dataPRB=dataPRB, dataJB = dataJB, headersJB = headersJB, selected_files = selected_files, jobs = partinfo[4])

if __name__ == '__main__':
    app.run(debug=False, host='phl-ws-0025', port=8050)


