import streamlit as st
from utils.download_sitemaps import download_sitemap
from utils.extract_urls_from_sitemap import process_sitemaps
from utils.scraperapi_scraper import scrape_and_convert_to_markdown
from utils.create_documents import create_documents
from utils.weaviate_utils import create_or_update_workspace_in_weaviate

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Generative AI Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Set up the Streamlit app title and sidebar
st.sidebar.title("Options")

if st.sidebar.button("Start Again"):
    if "downloaded_sitemaps" in st.session_state and st.session_state["downloaded_sitemaps"]:
        del st.session_state["downloaded_sitemaps"]

def initialize_session_state():
    if "downloaded_sitemaps" in st.session_state and st.session_state["downloaded_sitemaps"]:
        return False
    else:
        st.session_state["downloaded_sitemaps"] = st.session_state.get("downloaded_sitemaps", {})
        return True
    
def download_and_process_sitemaps(sitemap_url):
    with st.status("Downloading and processing sitemaps..."):
        try:
            st.write("Downloading sitemaps...")
            download_sitemap(sitemap_url, st.session_state.downloaded_sitemaps)

            st.write("Extracting URLs from each sitemap...")
            process_sitemaps(st.session_state.downloaded_sitemaps)
        except Exception as e:
            st.error(f"An error occurred during sitemap download or processing: {e}")

def scrape_markdown_and_index():
    with st.status("Scraping Markdown for Each URL..."):
        try:
            for filename, sitemap_data in st.session_state.downloaded_sitemaps.items():
                st.write(f"Processing sitemap {filename}...")
                sitemap_data.setdefault('scraped_markdowns', [])
                urls = sitemap_data.get('extracted_urls', [])
                for index, url in enumerate(urls):
                    st.write(f"**Processing URL {index + 1}/{len(urls)}...**")
                    if url.endswith('.xml'):
                        st.write(f"Skipping URL as it ends with .xml: {url}")
                        continue

                    st.write(f"Scraping markdown for URL: {url}")
                    scraped_content = scrape_and_convert_to_markdown(url)

                    if scraped_content:
                        st.success(f"Done! Displaying half body of the scraped content...")
                        half_length = len(scraped_content) // 2
                        displayed_content = scraped_content[:half_length]
                        st.markdown(f"```{displayed_content}```")
                        sitemap_data['scraped_markdowns'].append({'url': url, 'markdown': scraped_content})

                        st.write(f"Indexing URL: {url}...")
                        docs = create_documents(markdown_content=scraped_content, url=url)
                        create_or_update_workspace_in_weaviate(docs=docs, base_url=url)
                    else:
                        st.warning(f"No content scraped for URL: {url}")
        except Exception as e:
            st.error(f"An error occurred during markdown scraping or indexing: {e}")

def display_downloaded_sitemaps():
    if "downloaded_sitemaps" in st.session_state:
        with st.expander("Downloaded Sitemaps"):
            for filename, sitemap_data in st.session_state.downloaded_sitemaps.items():
                st.subheader(f"Sitemap: {filename}")
                st.text(sitemap_data['xml_content'])
                st.json(sitemap_data.get('extracted_urls', []))
                st.json(sitemap_data.get('scraped_markdowns', []))

def main():
    st.title("Sitemap Downloader")
    sitemap_url = st.text_input("Enter the sitemap URL", "")

    if st.button("Download Sitemaps"):
        if initialize_session_state():
            download_and_process_sitemaps(sitemap_url)
            scrape_markdown_and_index()
        else:
            st.info("Please click 'Start Again' from the sidebar to process a new sitemap.")

    display_downloaded_sitemaps()

if __name__ == "__main__":
    main()