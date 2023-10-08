import os
import glob
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
from fastapi import File, UploadFile
import shutil
#os.environ["OPENAI_API_KEY"] = "sk-"

def loadPdf(path):
    pdf_loader = PyPDFLoader(path)
    return pdf_loader.load()

def getPDFPages(file):
    pdf = PdfReader(file)
    pages =[]
    for page in pdf.pages:
        pages.append(page.extract_text())

    return pages
def splitDocuments(documents: [str]):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    createdDocuments = text_splitter.create_documents(documents)
    return text_splitter.split_documents(createdDocuments)

def getFilesAsString(path: str):
    fileContents = []

    for filename in glob.glob(os.path.join(path, '*.pdf')):
        with open(os.path.join(os.getcwd(), filename), 'rb') as f: # open in readonly mode
            fileContents.append(getPDFPages(f))

    return fileContents    

def saveFile(path, file: UploadFile):
    with open(path+"/"+file.filename,'wb') as output:
        shutil.copyfileobj(file.file, output)
        output.close()

def getFiles(path: str):
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return onlyfiles
