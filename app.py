from flask import Flask, render_template, request, redirect, url_for
import os
import json
from data_file import part
from excelBuilder import pnrn
import openpyxl
from findfile import get_latest_file_path, id_list_from_file
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
        revision_number = request.form['revisionNumber']
        dropdown_value = request.form['dropdown_value']
        filepaths = get_latest_file_path(part_number,dropdown_value)
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
        # part(part_number, revision_number, selected_files)
        workbook_pathPRB = f'C:\FinalVsCodeProject\PRB,{part_number},{revision_number}.xlsx'
        workbook_pathJB = f'C:\FinalVsCodeProject\JB,{part_number},{revision_number}.xlsx' 
        
        workbookPRB = openpyxl.load_workbook(workbook_pathPRB)
        workbookJB = openpyxl.load_workbook(workbook_pathJB)
        sheetPRB = workbookPRB.active
        sheetJB = workbookJB.active
        sheetPRB.delete_rows(2, sheetPRB.max_row)
        sheetJB.delete_rows(2, sheetJB.max_row)
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

        selected_files = request.args.getlist('selected_files')
        dropdown = request.args.get('dropdown_value')
        part_number = request.args.get('part_number')
        revision_number = request.args.get('revision_number')
        

        
        part(part_number, revision_number, selected_files)

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
                                headersPRB=headersPRB, dataPRB=dataPRB, dataJB = dataJB, headersJB = headersJB, selected_files = selected_files)

if __name__ == '__main__':
    app.run(debug=True)
    # , host='phl-ws-0025', port=8050



