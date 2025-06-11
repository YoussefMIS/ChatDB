# ChatDB

ChatDB is a Streamlit-based web application that allows you to chat with your database using natural language. It leverages LLMs (Large Language Models), Google Generative AI, Pinecone vector search, and LangChain to generate SQL queries and answer questions about your database schema and data.

## Features
- **Conversational SQL Generation:** Ask questions in plain English and get SQL queries or database insights.
- **Chat History:** Maintains a history of your questions and answers for context-aware conversations.
- **Database Schema Awareness:** Uses your schema and sample SQL to provide accurate, context-aware answers.
- **Powered by Megasoft:** Custom branding and UI enhancements.

## How It Works
1. **Ingestion:** The schema and sample SQL are loaded and split into chunks, embedded using Google Generative AI, and indexed in Pinecone.
2. **Chat:** User queries are processed by a language model, which retrieves relevant context from Pinecone and generates a response or SQL query.

## Setup Instructions

### Prerequisites
- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [Pinecone](https://www.pinecone.io/) account and API key
- [Google Generative AI](https://ai.google.dev/) API key
- Required Python packages (see below)

### Installation
1. **Clone the repository:**
   ```sh
   git clone <the-repo-url>
   cd chatdb
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   *(Create a `requirements.txt` with the following main packages:)*
   - streamlit
   - python-dotenv
   - langchain
   - langchain-google-genai
   - langchain-pinecone
   - pinecone-client

3. **Set up environment variables:**
   Create a `.env` file in the root directory with:
   ```env
   INDEX_NAME=your_pinecone_index_name
   GOOGLE_API_KEY=your_google_genai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENV=your_pinecone_environment
   ```

4. **Prepare your schema and SQL files:**
   - Place your schema in `schema.txt` and sample SQL in `sql.txt` in the project root.

5. **Ingest your data:**
   ```sh
   python ingestion.py
   ```

6. **Run the app:**
   ```sh
   streamlit run main.py
   ```

## File Structure
- `main.py` — Streamlit app UI and chat logic
- `backend/core.py` — LLM and retrieval chain logic
- `ingestion.py` — Loads and embeds schema and SQL into Pinecone
- `schema.txt` — Your database schema description
- `sql.txt` — Sample SQL statements

## License
See [LICENSE.txt](LICENSE.txt) for details.

## Acknowledgements
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Google Generative AI](https://ai.google.dev/)
- [Pinecone](https://www.pinecone.io/)

---
*Powered by Megasoft*
