import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from config import llm  # Import the shared LLM instance from config.py
from langchain_mistralai import MistralAIEmbeddings
load_dotenv() # Loads GOOGLE_API_KEY from .env

DB_PATH = "./chroma_db"
POLICY_FILE = "./data/sample_policy.pdf"



# This handles the PDF searching
embeddings = MistralAIEmbeddings(
    model="mistral-embed", 
    mistral_api_key=os.getenv("MISTRAL_API_KEY")
)


if not os.path.exists(DB_PATH):
    loader = PyPDFLoader(POLICY_FILE)
    splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(loader.load())
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=DB_PATH)
else:
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)


retriever = vectorstore.as_retriever(search_kwargs={"k": 3})