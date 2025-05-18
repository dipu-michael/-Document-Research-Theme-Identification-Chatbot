import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

# Get OpenAI API key
openai_api_key = os.getenv("CHROMA_OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("CHROMA_OPENAI_API_KEY is not set in .env file")

# Initialize OpenAI v1 client
client = OpenAI(api_key=openai_api_key)

# Define Chroma embedding function
embedding_func = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-3-small"
)

# Set up ChromaDB client and document collection
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="document_chunks",
    embedding_function=embedding_func
)

def query_documents(user_query):
    """
    Answers a user question by searching embedded document chunks and passing context to GPT.

    Args:
        user_query (str): The natural language question from the user.

    Returns:
        tuple: (Answer string, list of document sources referenced)
    """
    # Search for top-matching chunks using vector similarity
    results = collection.query(query_texts=[user_query], n_results=5)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Construct GPT input context
    context = ""
    sources = set()

    for doc, meta in zip(documents, metadatas):
        context += doc + "\n"
        sources.add(meta.get("source", "unknown"))

    prompt = f"""
You are an expert research assistant. Use the provided document content to answer the user's question.
Cite document names in square brackets like [source.pdf].

Context:
{context}

Question: {user_query}
Answer:
"""

    # Query GPT-4
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    answer = response.choices[0].message.content
    return answer, list(sources)
