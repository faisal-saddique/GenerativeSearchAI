import os
from dotenv import load_dotenv
from typing import List
from langchain_core.documents import Document
from langchain_community.retrievers import (
    WeaviateHybridSearchRetriever,
)
import weaviate
import logging
import streamlit as st
from utils.scraperapi_scraper import extract_base_url
import re

load_dotenv()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")

auth_client_secret = weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY"))

def get_weaviate_retriever(top_k: int, client: weaviate.Client, selected_class) -> WeaviateHybridSearchRetriever:
    retriever = WeaviateHybridSearchRetriever(
        client=client,
        index_name=selected_class,
        text_key="text",
        attributes=["gsc_source_url"],
        create_schema_if_missing=True,
        k=top_k
    )
    return retriever

def create_or_update_workspace_in_weaviate(docs: List[Document], base_url) -> str:
    try:
        client = weaviate.Client(
            url=WEAVIATE_URL,
            additional_headers={
                "X-Openai-Api-Key": os.getenv("OPENAI_API_KEY"),
            },
            auth_client_secret=auth_client_secret
        )
        # st.write("Weaviate client successfully created.")
    except Exception as e:
        logging.exception(f"Weaviate client creation failed: {e}")
        st.error("Failed to create Weaviate client.")
        return "Weaviate client creation failed."
    # Remove symbols from the base URL and convert the result to uppercase
    clean_base_url = re.sub(r'[^\w\s]', '', extract_base_url(url=base_url)).upper()
    index_name = f"GSC_{clean_base_url}"
    st.write(f"Index name for Weaviate set to: {index_name}")

    retriever = WeaviateHybridSearchRetriever(
        client=client,
        index_name=index_name,
        text_key="text",
        attributes=[],
        create_schema_if_missing=True,
    )

    chunk_size = 1000
    total_docs = len(docs)
    st.write(f"Total number of documents to index: {total_docs}")

    for start in range(0, total_docs, chunk_size):
        end = min(start + chunk_size, total_docs)
        chunk = docs[start:end]
        chunk_number = start // chunk_size + 1
        total_chunks = (total_docs - 1) // chunk_size + 1

        st.write(f"Pushing chunk {chunk_number} of {total_chunks} ({len(chunk)} documents)")

        try:
            retriever.add_documents(chunk)
            st.write(f"Chunk {chunk_number} pushed successfully.")
        except Exception as e:
            logging.exception(f"Failed to push chunk {chunk_number}: {e}")
            st.error(f"Failed to push chunk {chunk_number}.")
    
    st.success("All documents have been successfully indexed in Weaviate.")
    return "Done!"

def query_weaviate(query: str, top_k: int, selected_class) -> List[Document]:
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

    retriever = get_weaviate_retriever(top_k=top_k, client=client, selected_class=selected_class)
    docs = retriever.get_relevant_documents(
        query=query,
        # where_filter=where_filter,
    )
    return docs