import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
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

#documents = loadPdf('./docs/RachelGreenCV.pdf')