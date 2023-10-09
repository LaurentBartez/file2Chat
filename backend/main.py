from enum import Enum
from fastapi import FastAPI, UploadFile, Query, status
from fastapi.responses import FileResponse
from typing import Annotated
import documentLoader
from database import Database
from pydantic import BaseModel
import responseGenerator


app = FastAPI()
documentPath = "./documents"

class AvailableFileTypes(str, Enum):
    pdf = "pdf"

class ChatRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ping", status_code=status.HTTP_204_NO_CONTENT)
async def ping():
    return

@app.get("/files/")
async def listFiles():
    db = Database()
    allFiles = documentLoader.getFiles(documentPath)
    return {"files":allFiles}

@app.get("/files/{fileName}")
async def getFile(fileName: str):
    # file = documentLoader.getFile(documentPath + "/" + fileName)#
    print (documentPath + "/" + fileName)
    return FileResponse(documentPath + "/" + fileName)

@app.post("/uploadFiles/")
async def uploadFile(file: UploadFile):
    documentLoader.saveFile(documentPath,file)
    fileContents = documentLoader.getFilesAsString(documentPath)
    db = Database()
    createdIDs = db.addMultipleDocuments(fileContents)
    return {"filename" : file.filename, "createdIDs": createdIDs}

@app.get("/chat/")
async def ask(prompt: str, history: Annotated[list[str], Query()] = []):
    rg = responseGenerator.ResponseGenerator()
    answer = rg.getResponse(prompt, history)
    return {"answer": answer}
