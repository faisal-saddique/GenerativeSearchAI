import os
from dotenv import load_dotenv
from typing import List
from langchain_core.documents import Document
from langchain_community.retrievers import (
    WeaviateHybridSearchRetriever,
)
from langchain_community.document_loaders import PyMuPDFLoader, CSVLoader, Docx2txtLoader
import weaviate
import logging

load_dotenv()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")

auth_client_secret = weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY"))

def get_weaviate_retriever(top_k: int, client: weaviate.Client) -> WeaviateHybridSearchRetriever:
    retriever = WeaviateHybridSearchRetriever(
        client=client,
        index_name="GSC_test",
        text_key="text",
        attributes=["gsc_source_url"],
        create_schema_if_missing=True,
        k=top_k
    )
    return retriever

def create_or_update_workspace_in_weaviate(docs: List[Document]) -> str:
    try:
        client = weaviate.Client(
            url=WEAVIATE_URL,
            additional_headers={
                "X-Openai-Api-Key": os.getenv("OPENAI_API_KEY"),
            },
            auth_client_secret=auth_client_secret
        )
    except Exception as e:
        logging.exception(f"Weaviate client creation failed: {e}")

    retriever = WeaviateHybridSearchRetriever(
        client=client,
        index_name="GSC_test",
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
        logging.info(
            f"Pushing chunk {start // chunk_size + 1} of {total_docs // chunk_size + 1}")
        logging.info(f"Chunk size: {len(chunk)} documents")

        retriever.add_documents(chunk)

        # Print a message after each chunk is pushed
        logging.info(f"Chunk {start // chunk_size + 1} pushed successfully.")
    
    return "Done!"

def query_weaviate(query: str, top_k: int) -> List[Document]:
    try:
        client = weaviate.Client(
            url=WEAVIATE_URL,
            additional_headers={
                "X-Openai-Api-Key": os.getenv("OPENAI_API_KEY"),
            },
            auth_client_secret=auth_client_secret
        )

    except Exception as e:
        logging.exception(f"Weaviate client creation failed: {e}")

    # Construct the 'operands' list for the 'where' filter
    # operands = [
    #     {
    #         "path": ["file_id"],
    #         "operator": "Equal",
    #         "valueString": file_id,
    #     } for file_id in file_ids
    # ]

    # Combine 'operands' using the 'or' operator
    # where_filter = {
    #     "operator": "Or",
    #     "operands": operands,
    # }

    retriever = get_weaviate_retriever(top_k=top_k, client=client)
    docs = retriever.get_relevant_documents(
        query=query,
        # where_filter=where_filter,
    )
    return docs
