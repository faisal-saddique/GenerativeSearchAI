import os
from utils.logger_setup import setup_logging
from utils.scraper import scrape_url_to_markdown
from utils.extract_urls_from_sitemap import extract_urls_from_sitemap
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.weaviate_utils import create_or_update_workspace_in_weaviate
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

def process_urls_and_update_weaviate(folder_path):
    """
    Extracts URLs from sitemap files in a folder, scrapes content, splits the content, and updates Weaviate.
    """
    try:
        processed_documents = []

        # Iterate through all XML files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".xml"):
                sitemap_path = os.path.join(folder_path, filename)
                logging.info(f"Processing sitemap: {sitemap_path}")

                # Extract URLs from the sitemap
                urls_to_scrape = extract_urls_from_sitemap(sitemap_path)
                logging.info(f"Extracted {len(urls_to_scrape)} URLs from the sitemap.")

                # Process each URL
                for url in urls_to_scrape:
                    try:
                        # Scrape the URL to Markdown
                        markdown_content = scrape_url_to_markdown(url)
                        if markdown_content:
                            # Split the Markdown content by headers
                            # md_header_splits = markdown_splitter.split_text(markdown_content)
                            # Further split the content into chunks
                            document_chunks = text_splitter.split_documents([Document(page_content=markdown_content, metadata={})])
                            # Add source URL metadata and update Weaviate
                            for chunk in document_chunks:
                                chunk.metadata['gsc_source_url'] = url
                            create_or_update_workspace_in_weaviate(document_chunks)
                            processed_documents.extend(document_chunks)
                            logging.info(f"Processed and updated Weaviate for URL: {url}")
                        else:
                            logging.warning(f"No content found for URL: {url}")
                    except Exception as e:
                        logging.error(f"Error processing URL {url}: {e}", exc_info=True)
        logging.info("All URLs processed and Weaviate updated.")
        return processed_documents
    except Exception as e:
        logging.error(f"Failed to process URLs from sitemaps: {e}", exc_info=True)
        return []

# Run the processing function
if __name__ == "__main__":
    FOLDER_PATH = "example_sitemaps_new"  # Update this with the path to your folder containing XML files
    processed_docs = process_urls_and_update_weaviate(FOLDER_PATH)
