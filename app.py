from flask import Flask, render_template, request, redirect, url_for
import os
import json
from data_file import part
from excelBuilder import pnrn

import openpyxl
directory_path = r"X:\PROGRAMMING\CUSTOMER"
dropdown = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]

app = Flask(__name__)
# data_file.engine

@app.route('/')
def form():
    return render_template('main.html', dropdown = dropdown)



@app.route('/submit-form', methods=['POST'])
def submit_form():
    part_number = request.form['partNumber']
    revision_number = request.form['revisionNumber']
    

    dropdown_value = request.form["dropdown"]
    dropdown_value = str(dropdown_value)
    datainfo = part(part_number, revision_number, dropdown_value)
    return redirect(url_for('success', file= datainfo[2], part_number=part_number, revision_number=revision_number, dropdown=dropdown_value))


    



@app.route('/success', methods=['GET', 'POST'])
def success():

    
    if request.method == 'POST':
        # Get the edited data from the form
        part_number = request.form.get('part_number')
        revision_number = request.form.get('revision_number')
        dropdown_value = request.form.get('dropdown')
        print(part_number, revision_number)
        edited_dataPRB = request.form.getlist('edited_dataPRB')
        edited_dataJB = request.form.getlist('edited_dataJB')
        # Load the Excel file
        workbook_pathPRB = f'C:\FinalVsCodeProject\PRB,{part_number},{revision_number}.xlsx'
        workbook_pathJB = f'C:\FinalVsCodeProject\JB,{part_number},{revision_number}.xlsx' 
        
        workbookPRB = openpyxl.load_workbook(workbook_pathPRB)
        workbookJB = openpyxl.load_workbook(workbook_pathJB)
        sheetPRB = workbookPRB.active
        sheetJB = workbookJB.active

        # Update the corresponding cells in the Excel sheet
        for i, value in enumerate(edited_dataPRB):
            row_number = i // sheetPRB.max_column + 2  # Add 2 to skip the header row
            col_number = i % sheetPRB.max_column + 1
            sheetPRB.cell(row=row_number, column=col_number).value = value
            

        for i, value in enumerate(edited_dataJB):
            row_number = i // sheetJB.max_column + 2  # Add 2 to skip the header row
            col_number = i % sheetJB.max_column + 1
            sheetJB.cell(row=row_number, column=col_number).value = value

        # Save the changes back to the Excel file
        workbookPRB.save(workbook_pathPRB)
        workbookJB.save(workbook_pathJB)

        # Redirect to the success page
        return 'An email Has been sent to Mark Dieckman.'
    else:
        # Get the initial data from the Excel sheet
        part_number = request.args.get('part_number')
        revision_number = request.args.get('revision_number')
        dropdown_value = request.args.get('dropdown')
        
        
        workbook_pathPRB = f'C:\FinalVsCodeProject\PRB,{part_number},{revision_number}.xlsx'
        workbook_pathJB = f'C:\FinalVsCodeProject\JB,{part_number},{revision_number}.xlsx' 

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
                               dropdown=dropdown_value, headersPRB=headersPRB, dataPRB=dataPRB, dataJB = dataJB, headersJB = headersJB)

if __name__ == '__main__':
    app.run(debug=True)
    # , host='phl-ws-0025', port=8050

