import os
import uuid
import openai
import tiktoken
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

# Load environment variables from root-level .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

# Retrieve the OpenAI API key
openai_api_key = os.getenv("CHROMA_OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("CHROMA_OPENAI_API_KEY is not set in .env file")

# Initialize OpenAI embedding function for ChromaDB
embedding_func = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-3-small"
)

# Create ChromaDB client and document collection
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="document_chunks",
    embedding_function=embedding_func
)

def chunk_text(text, max_tokens=300):
    """
    Splits a large block of text into smaller chunks based on token count.
    Each chunk will be at most `max_tokens` tokens long.

    Args:
        text (str): The input text to split.
        max_tokens (int): Maximum number of tokens per chunk.

    Returns:
        List[str]: List of text chunks.
    """
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    words = text.split()
    chunks = []
    chunk = []
    tokens = 0

    for word in words:
        token_count = len(enc.encode(word + " "))
        if tokens + token_count > max_tokens:
            chunks.append(" ".join(chunk))
            chunk = []
            tokens = 0
        chunk.append(word)
        tokens += token_count

    if chunk:
        chunks.append(" ".join(chunk))

    return chunks

def add_text_to_chroma(document_name, text):
    """
    Adds extracted text into ChromaDB after splitting it into chunks.

    Args:
        document_name (str): Name of the document (used as source metadata).
        text (str): Full extracted text to embed.

    Returns:
        int: Number of chunks embedded.
    """
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        doc_id = f"{document_name}_{i}_{uuid.uuid4().hex}"
        collection.add(
            documents=[chunk],
            ids=[doc_id],
            metadatas=[{"source": document_name}]
        )
    return len(chunks)
