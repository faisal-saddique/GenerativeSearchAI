import xml.etree.ElementTree as ET
import streamlit as st

def extract_urls_from_sitemap(xml_content):
    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Dynamically find the namespace
    namespace = ''
    if root.tag.startswith('{'):
        namespace = root.tag.split('}')[0] + '}'

    urls = []
    # Check if this is a sitemap index file
    if root.tag == f'{namespace}sitemapindex':
        for sitemap in root.findall(f'{namespace}sitemap'):
            loc = sitemap.find(f'{namespace}loc').text
            urls.append(loc)
    # Otherwise, it's a standard sitemap file
    else:
        for url in root.findall(f'{namespace}url'):
            loc = url.find(f'{namespace}loc').text
            urls.append(loc)

    return urls

def process_sitemaps(sitemaps):
    for filename, sitemap_data in sitemaps.items():
        st.write(f"Extracting URLs for {filename}")
        # Extract URLs from the xml_content
        extracted_urls = extract_urls_from_sitemap(sitemap_data['xml_content'])
        # Place them in the sitemap_data under 'extracted_urls'
        sitemap_data['extracted_urls'] = extracted_urls
