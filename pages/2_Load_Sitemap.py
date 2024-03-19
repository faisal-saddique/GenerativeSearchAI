import streamlit as st
from utils.download_sitemaps import download_sitemap
from utils.extract_urls_from_sitemap import process_sitemaps
from utils.scraperapi_scraper import scrape_and_convert_to_markdown
from utils.create_documents import create_documents
from utils.weaviate_utils import create_or_update_workspace_in_weaviate

def initialize_session_state():
    if "downloaded_sitemaps" not in st.session_state:
        st.session_state["downloaded_sitemaps"] = {}

def download_and_process_sitemaps(sitemap_url):
    initialize_session_state()
    with st.status("Downloading Sitemaps..."):
        download_sitemap(sitemap_url, st.session_state["downloaded_sitemaps"])
    with st.status("Extracting URLs from each sitemap..."):
        process_sitemaps(st.session_state["downloaded_sitemaps"])

def scrape_markdown_and_index():
    with st.status("Scraping content from each URL and storing it to Weaviate..."):
        for filename, sitemap_data in st.session_state["downloaded_sitemaps"].items():
            sitemap_data.setdefault('scraped_markdowns', [])
            urls = sitemap_data.get('extracted_urls', [])
            for index, url in enumerate(urls):
                st.write(f"Processing URL {index}/{len(urls)}...")
                try:
                    st.write(f"Scraping markdown for URL: {url}")
                    scraped_content = scrape_and_convert_to_markdown(url=url)
                    if scraped_content:
                        st.info(f"Done! Displaying first 400 chars of the scraped content...")
                        st.write(f"{scraped_content[:400]}...")
                        sitemap_data['scraped_markdowns'].append({'url': url, 'markdown': scraped_content})
                        st.write(f"Indexing URL: {url}...")
                        docs = create_documents(markdown_content=scraped_content, url=url)
                        create_or_update_workspace_in_weaviate(docs=docs, base_url=url)
                except Exception as e:
                    st.error(f"An error occurred while processing {url}: {e}")

def display_downloaded_sitemaps():
    if "downloaded_sitemaps" in st.session_state:
        with st.expander("Downloaded Sitemaps"):
            for filename, sitemap_data in st.session_state["downloaded_sitemaps"].items():
                st.subheader(f"Sitemap: {filename}")
                st.text(sitemap_data['xml_content'])
                st.json(sitemap_data.get('extracted_urls', []))
                st.json(sitemap_data.get('scraped_markdowns',[]))

def main():
    st.title("Sitemap Downloader")
    sitemap_url = st.text_input("Enter the sitemap URL", "")

    if st.button("Download Sitemaps"):
        download_and_process_sitemaps(sitemap_url)
        scrape_markdown_and_index()

    display_downloaded_sitemaps()

if __name__ == "__main__":
    main()