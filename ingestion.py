import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

if __name__ == "__main__":
    print("Ingesting...")
    schemaloader = TextLoader(r"C:\Users\Lobna\chatdb\schema.txt", encoding="utf-8")
    sqlloader = TextLoader(r"C:\Users\Lobna\chatdb\sql.txt", encoding="utf-8")
    schemadocument = schemaloader.load()
    sqldocument = sqlloader.load()

    print("Splitting...")
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0, separator="\n\n"
    )
    texts = text_splitter.split_documents(schemadocument)
    texts += text_splitter.split_documents(sqldocument)
    texts = [text for text in texts if text.page_content.strip() != ""]
    print(f"Created {len(texts)} chunks")

    print("Embedding...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    print("Ingesting...")
    PineconeVectorStore.from_documents(
        texts, embeddings, index_name=os.environ["INDEX_NAME"]
    )
    print("Finished")
