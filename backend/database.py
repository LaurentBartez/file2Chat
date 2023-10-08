import chromadb
import uuid
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings
import documentLoader



class Database():
    def __init__(self):
        self.persistDirectory = "./db"
        self.client = chromadb.PersistentClient(path=self.persistDirectory)
        self.documents = self.client.get_or_create_collection(name = "documents")
        self.embeddings = GPT4AllEmbeddings()


    def addDocuments(self, docs: [str]):
        # create unique ids for each document based on content
        docs = documentLoader.splitDocuments(docs)
        ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in docs]
        unique_ids = list(set(ids))
        # Ensure that only docs that correspond to unique ids are kept and that only one of the duplicate ids is kept
        seen_ids = set()
        unique_docs = [doc for doc, id in zip(docs, ids) if id not in seen_ids and (seen_ids.add(id) or True)]
        vectorDb = Chroma.from_documents(unique_docs, self.embeddings, ids=unique_ids, persist_directory=self.persistDirectory)
        vectorDb.persist()
        return unique_ids
    
    def getCollections(self):
        return self.client.list_collections()
    
    def getFiles(self):
        files = []
        for collection in self.client.list_collections():
            vectorCollection = self.client.get_collection(collection.name)
            data = vectorCollection.get()
            files.append({"collection": collection, "data": data})
        return files





