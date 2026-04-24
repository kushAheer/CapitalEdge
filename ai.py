import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from langchain_text_splitters import RecursiveCharacterTextSplitter

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_pinecone import PineconeEmbeddings


from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage




load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


class ChatBot:
    def __init__(self):
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is missing in environment variables.")
        if not pinecone_api_key:
            raise ValueError("PINECONE_API_KEY is missing in environment variables.")

        self.documents = []

        self.llmModel = ChatGroq(
            api_key=groq_api_key,
            model="llama-3.3-70b-versatile",
            temperature=0
        )

        self.pinecone = Pinecone(api_key=pinecone_api_key)
        idx_name = "coinwise"

        existing_indexes = set(self.pinecone.list_indexes().names())
        if idx_name not in existing_indexes:
            self.pinecone.create_index(
                name=idx_name,
                dimension=1024,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=os.getenv("PINECONE_CLOUD", "aws"),
                    region=os.getenv("PINECONE_REGION", "us-east-1")
                ),
            )

        self.embeddings = PineconeEmbeddings(model="multilingual-e5-large") 

        index = self.pinecone.Index(idx_name)
        self.vectorStore = PineconeVectorStore(embedding=self.embeddings , index=index)

        self.chat_history = []

        self.system_prompt = """
You are a financial analyst assistant. Answer questions strictly using the bank statement context provided.

Rules:
- Always include amounts with currency symbols.
- If asked about totals, sum up the relevant transactions shown in context.
- If the answer is not in the context, say "This information is not in the provided statement."
- Never make up transaction details, balances, or dates.
- Format amounts consistently (e.g. ₹1,24,500 or $1,245.00).
"""

        self.rag_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "human",
                    "Context:\n{context}\n\nQuestion: {question}\nAnswer:",
                ),
            ]
        )
    
    def load_document(self , pdf : str):
        loader = PyPDFLoader(pdf)
        self.documents = loader.load()
        return self.documents
        
    def split_document(self , pdf : str = ""):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.documents = text_splitter.split_documents(self.documents)
        return self.documents
    
    def embed_and_store(self , pdf : str = ""):
        if not self.documents:
            raise ValueError("No documents found. Load and split documents before embedding.")
        self.vectorStore.add_documents(self.documents)
        return True
    
    def chat(self , query : str):
        retriever = self.vectorStore.as_retriever(search_kwargs={"k": 4})
        relevant_docs = retriever.invoke(query)
        context = "\n\n".join(doc.page_content for doc in relevant_docs)

        chain = self.rag_prompt | self.llmModel
        response = chain.invoke(
            {
                "chat_history": self.chat_history,
                "context": context,
                "question": query,
            }
        )

        self.chat_history.append(HumanMessage(content=query))
        self.chat_history.append(AIMessage(content=response.content))
        return response.content