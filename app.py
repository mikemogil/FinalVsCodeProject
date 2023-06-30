from flask import Flask, render_template, request, redirect, url_for
import os
from data_file import part

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
    print(dropdown_value)
    datainfo = part(part_number, dropdown_value)
    return redirect(url_for('success', file= datainfo[2], part_number=part_number, revision_number=revision_number, dropdown=dropdown_value))
def partnumber():
    return part_number
@app.route('/success')
def success():
    latest_file_path = request.args.get('file')
    part_number = request.args.get('part_number')
    revision_number = request.args.get('revision_number')
    
    dropdown_value = request.args.get('dropdown')
    print(latest_file_path)
    return render_template('excel.html',part_number=part_number, revision_number=revision_number, dropdown=dropdown_value)

if __name__ == '__main__':
    app.run()
