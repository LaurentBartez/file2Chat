from enum import Enum
from fastapi import FastAPI, UploadFile, Query, status
from typing import Annotated
import documentLoader
from database import Database
from pydantic import BaseModel
import responseGenerator


app = FastAPI()

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
    allFiles = db.getFiles()
    return {"collections":allFiles}

@app.get("/files/{itemID}")
async def getFile(itemID: int):
    fileType = AvailableFileTypes.pdf
    return {"itemID": itemID, "fileType": fileType}

@app.post("/uploadFiles/")
async def uploadFile(file: UploadFile):
    pages = documentLoader.getPDFPages(file.file)
    db = Database()
    createdIDs = db.addDocuments(pages)
    return {"filename" : file.filename, "createdIDs": createdIDs}

@app.get("/chat/")
async def ask(prompt: str, history: Annotated[list[str], Query()] = []):
    rg = responseGenerator.ResponseGenerator()
    answer = rg.getResponse(prompt, history)
    return {"answer": answer}
