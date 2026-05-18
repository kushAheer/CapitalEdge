import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from langchain_text_splitters import RecursiveCharacterTextSplitter

from pinecone import Pinecone, ServerlessSpec
# pyright: ignore [reportMissingImports]
from langchain_pinecone import PineconeVectorStore
# pyright: ignore [reportMissingImports]
from langchain_pinecone import PineconeEmbeddings


from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage




load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


class ChatBot:
    def __init__(self, user_id: str):
        """
        Initialize ChatBot for a specific user.

        Args:
            user_id: A unique identifier for the user (e.g. username, UUID, email).
                     All documents and queries are scoped to this user's namespace,
                     so no user can access another user's data.
        """
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is missing in environment variables.")
        if not pinecone_api_key:
            raise ValueError("PINECONE_API_KEY is missing in environment variables.")
        if not user_id or not user_id.strip():
            raise ValueError("user_id must be a non-empty string.")

        # Sanitize user_id: Pinecone namespaces allow alphanumerics, hyphens,
        # and underscores. Replace anything else to avoid API errors.
        self.namespace = "user_" + "".join(
            c if c.isalnum() or c in "-_" else "_" for c in user_id.strip()
        )

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

        # Scope the vector store to this user's namespace.
        # Every upsert and query will be isolated to self.namespace,
        # so users cannot read each other's documents.
        self.vectorStore = PineconeVectorStore(
            embedding=self.embeddings,
            index=index,
            namespace=self.namespace,   # <-- per-user isolation
        )

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

    def load_document(self, pdf: str):
        loader = PyPDFLoader(pdf)
        loaded_documents = loader.load()
        self.documents = [
            document
            for document in loaded_documents
            if document.page_content and document.page_content.strip()
        ]

        if not loaded_documents:
            raise ValueError("No pages were found in the uploaded PDF.")

        if not self.documents:
            raise ValueError(
                "No readable text was found in the uploaded PDF. "
                "It may be scanned, image-only, or password protected."
            )

        return self.documents

    def split_document(self, pdf: str = ""):
        if not self.documents:
            raise ValueError("No readable document text found. Upload a text-based PDF before indexing.")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        split_documents = text_splitter.split_documents(self.documents)
        self.documents = [
            document
            for document in split_documents
            if document.page_content and document.page_content.strip()
        ]

        if not self.documents:
            raise ValueError("No text chunks could be created from the uploaded PDF.")

        return self.documents

    def embed_and_store(self, pdf: str = ""):
        if not self.documents:
            raise ValueError("No document chunks found. Load and split a readable PDF before embedding.")
        # Documents are stored under self.namespace automatically
        # because the vectorStore was constructed with namespace=self.namespace.
        self.vectorStore.add_documents(self.documents)
        return True

    def chat(self, query: str):
        # Retrieval is also scoped to self.namespace — users only see their own data.
        retriever = self.vectorStore.as_retriever(search_kwargs={"k": 4})
        relevant_docs = retriever.invoke(query)

        context = ""
        for doc in relevant_docs:
            context += doc.page_content + "\n\n"

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

    def clear_user_data(self):
        """
        Delete all vectors stored under this user's namespace.
        Useful when a user wants to reset or delete their data.
        """
        index = self.pinecone.Index("coinwise")
        index.delete(delete_all=True, namespace=self.namespace)
