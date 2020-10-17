from fastapi import FastAPI, File, UploadFile
import uvicorn
import uuid
import program

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the homepage"}


@app.post("/uploadfile")
def create_upload_file(file: UploadFile = File(...)):
    df = program.run2(file)
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
