import os
from utils.logger_setup import setup_logging
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.documents import Document
import logging

# Initialize logging
setup_logging()

# Constants
HEADER_SPLIT_CONFIG = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 20

# Initialize text splitters
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADER_SPLIT_CONFIG, strip_headers=False)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

def create_documents(markdown_content, url):
    document_chunks = text_splitter.split_documents([Document(page_content=markdown_content, metadata={})])
    # Add source URL metadata and update Weaviate
    for chunk in document_chunks:
        chunk.metadata['gsc_source_url'] = url

    return document_chunks

