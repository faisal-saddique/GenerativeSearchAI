import xml.etree.ElementTree as ET

def extract_urls_from_sitemap(xml_file_path):
    # Parse the XML content from the file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

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