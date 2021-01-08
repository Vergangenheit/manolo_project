from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.datastructures import FileStorage
from program import process
import os

app: Flask = Flask(__name__)


@app.route("/")
def home():
    return render_template('main.html')


@app.route("/", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        uploaded_file: FileStorage = request.files.get("file")
        process(uploaded_file.stream, True)
        # TODO return excel file of df from process function and send it to download view
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
