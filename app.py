from flask import Flask, render_template, request, redirect, url_for
# from data_file import part

from data_file import BindParam

app = Flask(__name__)
part_number = ''
# data_file.engine
def partnumber():
    return partnumber
@app.route('/')
def form():
    return render_template('main.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    part_number = request.form['partNumber']
    revision_number = request.form['revisionNumber']
    dropdown = request.form['dropdown']
    # data_file.part(part_number)
    # datainfo = data_file.dataB()
    rowsPart = BindParam()
    print(rowsPart)
    return redirect(url_for('success', file= "yo wasgood", part_number=part_number, revision_number=revision_number, dropdown=dropdown))
def partnumber():
    return part_number
@app.route('/success')
def success():
    latest_file_path = request.args.get('file')
    part_number = request.args.get('part_number')
    revision_number = request.args.get('revision_number')
    dropdown = request.args.get('dropdown')
    print(latest_file_path)
    return render_template('excel.html',part_number=part_number, revision_number=revision_number, dropdown=latest_file_path)

if __name__ == '__main__':
    app.run()
