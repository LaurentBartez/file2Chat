from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings
from database import Database

class ResponseGenerator():

    def __init__(self):
        self.local_path = (
        "./models/llama-2-7b-chat.ggmlv3.q4_0.bin"  # replace with your desired local file path
        )
        self.callbacks = [StreamingStdOutCallbackHandler()]
        self.chain = self.makeChain()
        self.chatHistory = []
 
    def makeChain(self):
        llm = GPT4All(model=self.local_path)
        myDb = Database()
        vectordb = Chroma(
            persist_directory=myDb.persistDirectory, embedding_function=myDb.embeddings
        )  
        retriever = vectordb.as_retriever(search_type ="similarity", search_kwargs={'k': 2})

        chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        verbose = True
        )
        return chain

    def getResponse(self, prompt: str, chatHistory: list[list[str]]):
        chat_history_tuples = []
        for message in chatHistory:
            chat_history_tuples.append((message[0], message[1]))
    
        result = self.chain({'question': prompt, 'chat_history': chat_history_tuples})
        self.chatHistory = [prompt, result['answer']]
        return result['answer']
    