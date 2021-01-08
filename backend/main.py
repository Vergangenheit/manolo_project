from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.datastructures import FileStorage
from program import process
from pandas import DataFrame

app: Flask = Flask(__name__)


@app.route("/")
def home():
    return render_template('main.html')


@app.route("/", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        uploaded_file: FileStorage = request.files.get("file")
        print(uploaded_file.filename)
        # TODO process file from it's stream without saving it to disk
        uploaded_file.save(dst=f'../data/{uploaded_file.filename}')
        process(f'../data/{uploaded_file.filename}', True)
    return redirect(url_for('file_downloads'))


@app.route('/file-download/', methods=["GET"])
def file_downloads():
    if request.method == "GET":
        try:
            return render_template('downloads.html')
        except Exception as e:
            return str(e)


@app.route('/return-file/', methods=["GET"])
def return_files_tut():
    if request.method == "GET":
        try:
            return send_file('../data/results.xlsx', attachment_filename='results.xlsx')
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    app.run(debug=True)
