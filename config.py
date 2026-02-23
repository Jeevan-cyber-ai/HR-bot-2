import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_mistralai import ChatMistralAI
# Load variables from .env file
load_dotenv()

llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0,
    mistral_api_key=os.getenv("MISTRAL_API_KEY")
)