from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings
import documentLoader


class responseGenerator():

    def __init__(self, pathOfDocument):
        self.documents = self.splitDocuments(pathOfDocument)
        self.local_path = (
        "./models/llama-2-7b-chat.ggmlv3.q4_0.bin"  # replace with your desired local file path
        )
        self.callbacks = [StreamingStdOutCallbackHandler()]
        self.chain = self.makeChain()
        self.chatHistory = []        

    def splitDocuments(self, path):
        loadedDocuments = documentLoader.loadPdf(path)
 
        # we split the data into chunks of 1,000 characters, with an overlap
        # of 200 characters between the chunks, which helps to give better results
        # and contain the context of the information between chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(loadedDocuments)

    def makeChain(self):
        llm = GPT4All(model=self.local_path, callbacks=self.callbacks, verbose=True)

        vectordb = Chroma.from_documents(
          self.documents,
          embedding=GPT4AllEmbeddings(),
          persist_directory='./data'
        )
        vectordb.persist()

        retriever = vectordb.as_retriever(search_type ="similarity", search_kwargs={'k': 2})

        chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        verbose = True
        )
        return chain

    def getResponse(self, prompt):
        result = self.chain({'question': prompt, 'chat_history': self.chatHistory})
        self.chatHistory = [prompt, result['answer']]
        return result['answer']
    