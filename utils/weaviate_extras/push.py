# Import required libraries
from dotenv import load_dotenv  # For loading environment variables from .env file
import os
import weaviate
from langchain_core.documents import Document
from langchain_community.retrievers import (
    WeaviateHybridSearchRetriever,
)
# Load environment variables from .env file
load_dotenv()

print(os.getenv("WEAVIATE_URL"))
print(os.getenv("WEAVIATE_API_KEY"))
      
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
auth_client_secret = weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY"))

client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={
        "X-Openai-Api-Key": os.getenv("OPENAI_API_KEY"),
    },
    auth_client_secret=auth_client_secret
)

docs = [Document(page_content="Hello",metadata={})]

print(f"Total chunks: {len(docs)}")

print(f"Pushing docs to Weaviate...")

retriever = WeaviateHybridSearchRetriever(
    client=client,
    index_name="Testing",
    text_key="text",
    attributes=[],
    create_schema_if_missing=True,
)

chunk_size = 1000
total_docs = len(docs)

for start in range(0, total_docs, chunk_size):
    end = min(start + chunk_size, total_docs)
    chunk = docs[start:end]
    
    # Print some information about the current chunk
    print(f"Pushing chunk {start // chunk_size + 1} of {total_docs // chunk_size + 1}")
    print(f"Chunk size: {len(chunk)} documents")
    
    retriever.add_documents(chunk)

    # Print a message after each chunk is pushed
    print(f"Chunk {start // chunk_size + 1} pushed successfully.")

print("All docs pushed to Pinecone.")
