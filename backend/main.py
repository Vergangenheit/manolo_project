from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.datastructures import FileStorage
from program import process, to_excel
import os
from pandas import DataFrame
import base64

app: Flask = Flask(__name__)


@app.route("/")
def home():
    return render_template('main.html')


@app.route("/", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        uploaded_file: FileStorage = request.files.get("file")
        result: DataFrame = process(uploaded_file.stream, False)
        val: bytes = to_excel(result)
        b64: bytes = base64.b64encode(val)
        return render_template('downloads.html', b64=b64)
    return redirect(url_for('file_downloads'))


@app.route('/file-download/', methods=["GET"])
def file_downloads():
    if request.method == "GET":
        try:
            return render_template('downloads.html')
        except Exception as e:
            return str(e)


@app.route('/return-file/', methods=["GET"])
def return_files():
    print(request.method)
    if request.method == "GET":
        try:
            send_file('../data/results.xlsx', attachment_filename='results.xlsx')
        except Exception as e:
            return str(e)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
