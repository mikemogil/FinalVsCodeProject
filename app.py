from flask import Flask, render_template, request, redirect, url_for
import os
import json
from data_file import part
import openpyxl
directory_path = r"X:\PROGRAMMING\CUSTOMER"
dropdown = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]

app = Flask(__name__)
part_number = ''
# data_file.engine
def partnumber():
    return partnumber
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
def partnumber():
    return part_number


@app.route('/success', methods=['GET', 'POST'])
def success():
    if request.method == 'POST':
        # Get the edited data from the form
        edited_data = request.form.getlist('edited_data[]')
        print(edited_data)
        # Load the Excel file
        workbook_path = 'C:\FinalVsCodeProject\data_sheet.xlsx'
        workbook = openpyxl.load_workbook(workbook_path)
        sheet = workbook.active

        # Update the corresponding cells in the Excel sheet
        for i, value in enumerate(edited_data):
            row_number = i // sheet.max_column + 2  # Add 2 to skip the header row
            col_number = i % sheet.max_column + 1
            sheet.cell(row=row_number, column=col_number).value = value

        # Save the changes back to the Excel file
        workbook.save(workbook_path)

        # Redirect to the success page
        return redirect('/success')
    else:
        # Get the initial data from the Excel sheet
        part_number = request.args.get('part_number')
        revision_number = request.args.get('revision_number')
        dropdown_value = request.args.get('dropdown')

        workbook_path = 'C:\FinalVsCodeProject\data_sheet.xlsx'
        workbook = openpyxl.load_workbook(workbook_path)
        sheet = workbook.active

        headers = [cell.value for cell in sheet[1]]
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(row)

        return render_template('excel.html', part_number=part_number, revision_number=revision_number,
                               dropdown=dropdown_value, headers=headers, data=data)

if __name__ == '__main__':
    app.run()

