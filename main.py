import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings,ChatOllama
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()

def format_docs(docs):
    """Format the documents for the custom RAG prompt."""
    return "\n\n".join([doc.page_content for i, doc in enumerate(docs)])

if __name__ == "__main__":
    template = """
    You are an agent designed to interact with an Oracle SQL database.
    Given an input question written in normal english, create a syntactically correct Oracle SQL query to run.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.

    
    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP, TRUNCATE etc.) to the database.
    To start you should ALWAYS look at the tables in the database to see what you can query.
    DO NOT make up some column names or table names. 
    Do NOT skip this step.
    When possible try to join tables to extend the retrieved information.
    Then you should generate the query from the schema of the most relevant tables.
    
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say you don't know, don't try to make up an answer:
    {context}
    
    Question: {question}"""

    custom_rag_prompt = PromptTemplate.from_template(template=template)


    print(" Retrieving...")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    llm = GoogleGenerativeAI(model="gemma-3-12b-it", google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0)

    query = "What is the total number of transactions per branch?"

    vectorstore = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME"], embedding=embeddings
    )

    rag_chain = (
        {"context": vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )
    # retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    # combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    # retrival_chain = create_retrieval_chain(
    #     retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    # ) | StrOutputParser()

    result = rag_chain.invoke(query)

    print("Query was:", query)
    print(result)