import os
import requests
from urllib.parse import urlparse
import xml.etree.ElementTree as ET  # For parsing XML content of sitemaps
import streamlit as st

# Headers for each request
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def find_potential_sitemap_urls(xml_content):
    """Parses XML content for sitemap URLs and filters potential XML sitemap URLs based on simple heuristics.

    Args:
        xml_content (str): The XML content of a sitemap.

    Returns:
        list: A list of potential sitemap URLs based on naming heuristics.
    """
    root = ET.fromstring(xml_content)
    namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    # Look for <loc> tags within <sitemap> elements
    urls = [elem.text for elem in root.findall('.//sitemap:loc', namespaces=namespace)]

    # Filter out URLs that are likely to be XML based on their patterns
    likely_xml_urls = [url for url in urls if url.endswith('.xml') or 'sitemap' in url.lower()]

    return likely_xml_urls

def check_if_xml(urls, headers):
    """Check if the given URLs are XML sitemaps by making network requests.

    Args:
        urls (list): A list of URLs to check.
        headers (dict): Request headers.

    Returns:
        list: A list of URLs confirmed to be XML sitemaps.
    """
    xml_urls = []
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            content_type = response.headers.get('content-type', '')
            if content_type.startswith('text/xml'):
                xml_urls.append(url)
        except Exception as e:
            print(f"Error fetching URL {url}: {e}")

    return xml_urls

def download_sitemap(url, sitemaps, downloaded_urls=set()):
    if url in downloaded_urls:
        print(f"Skipping already downloaded sitemap: {url}")
        return None  # Return None to indicate skipping

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Extract filename from URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path) or 'index'

            # Remove .xml extension if present in the filename
            if filename.endswith('.xml'):
                filename = filename[:-4]

            # Create filename with appropriate extension (assuming XML for sitemaps)
            sitemap_filename = f"{filename}.xml"  # Ensure the extension is .xml

            # Ensure that sitemaps[sitemap_filename] is a dictionary
            if sitemap_filename not in sitemaps:
                sitemaps[sitemap_filename] = {}  # Initialize a new dictionary for this filename

            sitemaps[sitemap_filename]['xml_content'] = response.content.decode()
            st.write(f"Sitemap downloaded successfully: {sitemap_filename}")

            downloaded_urls.add(url)  # Mark this URL as downloaded

            child_potential_sitemap_urls = find_potential_sitemap_urls(response.content.decode())
            child_sitemap_urls = check_if_xml(child_potential_sitemap_urls, headers=headers)
            for child_url in child_sitemap_urls:
                child_sitemaps = download_sitemap(child_url, sitemaps, downloaded_urls)
                if child_sitemaps:  # Merge child sitemaps if any
                    sitemaps.update(child_sitemaps)

        else:
            st.error(f"Failed to download sitemap. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    if url in downloaded_urls:
        print(f"Skipping already downloaded sitemap: {url}")
        return None  # Return None to indicate skipping

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Extract filename from URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path) or 'index'

            # Remove .xml extension if present in the filename
            if filename.endswith('.xml'):
                filename = filename[:-4]

            # Create filename with appropriate extension (assuming XML for sitemaps)
            sitemap_filename = f"{filename}.xml"  # Ensure the extension is .xml

            sitemaps[sitemap_filename]['xml_content'] = response.content.decode()
            print(f"Sitemap downloaded successfully: {sitemap_filename}")

            downloaded_urls.add(url)  # Mark this URL as downloaded

            child_potential_sitemap_urls = find_potential_sitemap_urls(response.content.decode())
            child_sitemap_urls = check_if_xml(child_potential_sitemap_urls, headers=headers)
            for child_url in child_sitemap_urls:
                child_sitemaps = download_sitemap(child_url, sitemaps, downloaded_urls)
                if child_sitemaps:  # Merge child sitemaps if any
                    sitemaps.update(child_sitemaps)

        else:
            st.error(f"Failed to download sitemap. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {e}")