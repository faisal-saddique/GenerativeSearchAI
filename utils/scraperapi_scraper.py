import os
import re
import requests
from urllib.parse import urlsplit
import html2text
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Extract base URL
def extract_base_url(url):
    parsed_url = urlsplit(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

# Filter out base64 images from HTML content
def filter_base64_images(html_content):
    base64_pattern = r'<img[^>]*src=["\']data:image/[^;]+;base64[^"\']*["\'][^>]*>'
    return re.sub(base64_pattern, '', html_content)

# Convert HTML to Markdown
def convert_html_to_markdown(html_content, base_url):
    h = html2text.HTML2Text()
    h.body_width = 0
    h.baseurl = base_url
    markdown_content = h.handle(filter_base64_images(html_content))
    return markdown_content

# Scrape content and convert to markdown
def scrape_and_convert_to_markdown(url):
    api_key = os.getenv('SCRAPERAPI_KEY')
    if not api_key:
        raise ValueError("API key not found in environment variables.")
    st.success(api_key)
    payload = {
        'api_key': api_key,
        'url': url,
        'render': True,
        'country_code': 'us',
        'device_type': 'desktop'
    }

    try:
        response = requests.get('https://api.scraperapi.com/', params=payload)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        st.error(f"Connection error occurred: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        st.error(f"Timeout error occurred: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error during requests to {url}: {req_err}")
        return None

    html_content = response.text
    base_url = extract_base_url(url)
    markdown_content = convert_html_to_markdown(html_content, base_url)
    return markdown_content