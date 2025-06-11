from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
import os

load_dotenv()
from typing import Any, Dict, List
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains.history_aware_retriever import create_history_aware_retriever

from typing import List

INDEX_NAME = os.environ["INDEX_NAME"]


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):

    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    chat = GoogleGenerativeAI(
        model="gemma-3-27b-it",
        google_api_key=os.environ["GOOGLE_API_KEY"],
        temperature=0,
    )

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    history_aware_retriever = create_history_aware_retriever(
        llm=chat,
        retriever=docsearch.as_retriever(search_kwargs={"k": 6}),
        prompt=rephrase_prompt,
    )
    qa = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )

    result = qa.invoke(input={"input": query, "chat_history": chat_history})
    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"],
    }
    return new_result


if __name__ == "__main__":
    res = run_llm(
        query="What is the total number of transactions per each branch name? generate an ORACLE SQL query to also display the top 5 results"
    )
    print(res["result"])
