from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

loader = PyPDFLoader("data/company_handbook.pdf")
docs = loader.load()
print(docs[0].page_content[:1000])
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="./chroma_db"
)

print("✅ Vector DB created")
