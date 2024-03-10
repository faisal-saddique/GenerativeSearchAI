import streamlit as st
import xml.etree.ElementTree as ET
import requests
from urllib.parse import urlparse
from utils.logger_setup import setup_logging

def is_valid_xml_sitemap_url(url):
    # Validate URL format
    try:
        result = urlparse(url)
        # Basic checks for scheme and netloc
        if not all([result.scheme, result.netloc]):
            return False, "Invalid URL format."
    except Exception as e:
        return False, str(e)
    
    # HTTP HEAD request to check content-type
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.head(url, headers=headers, timeout=5)
        content_type = response.headers.get('Content-Type', '')
        if 'xml' not in content_type:
            return False, "URL does not point to XML content."
    except requests.RequestException as e:
        return False, f"HTTP request failed: {str(e)}"
    
    # If all checks pass
    return True, "URL is a valid XML sitemap URL."

def parse_xml(content, is_string=False):
    # Parse the XML content based on input type
    root = ET.fromstring(content) if is_string else ET.parse(content).getroot()

    # Dynamically find the namespace
    namespace = ''
    if root.tag.startswith('{'):
        namespace = root.tag.split('}')[0] + '}'

    urls = []
    if root.tag == f'{namespace}sitemapindex':
        for sitemap in root.findall(f'{namespace}sitemap'):
            loc = sitemap.find(f'{namespace}loc').text
            urls.append(loc)
    else:
        for url in root.findall(f'{namespace}url'):
            loc = url.find(f'{namespace}loc').text
            urls.append(loc)
    return urls

def fetch_sitemap(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return parse_xml(response.text, is_string=True), None
    except Exception as e:
        return [], str(e)

setup_logging()

st.title("Sitemap Parser")

option = st.radio("Choose an option:", ('Enter Sitemap URL', 'Upload XML File'))

if option == 'Enter Sitemap URL':
    sitemap_url = st.text_input("Enter the sitemap URL:", "")
    if st.button("Fetch and Parse"):
        if sitemap_url:
            is_valid, message = is_valid_xml_sitemap_url(sitemap_url)
            if is_valid:
                urls, error = fetch_sitemap(sitemap_url)
                if error:
                    st.error(f"Failed to fetch sitemap: {error}")
                elif urls:
                    with st.expander("Found URLs"):
                        for url in urls:
                            st.write(url)
                else:
                    st.warning("No URLs found in the sitemap.")
            else:
                st.error(message)
                st.stop()
        else:
            st.warning("Please enter a valid URL.")

elif option == 'Upload XML File':
    uploaded_file = st.file_uploader("Choose an XML file", type=['xml'])
    if uploaded_file:
        urls = parse_xml(uploaded_file)
        if urls:
            with st.expander("Found URLs"):
                for url in urls:
                    st.write(url)
        else:
            st.warning("No URLs found in the uploaded file.")

