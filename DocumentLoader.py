import os
from langchain.document_loaders import PyPDFLoader

#os.environ["OPENAI_API_KEY"] = "sk-"

def loadPdf(path):
    pdf_loader = PyPDFLoader(path)
    return pdf_loader.load()


#documents = loadPdf('./docs/RachelGreenCV.pdf')