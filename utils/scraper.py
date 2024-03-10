import re
import time
from urllib.parse import urlsplit
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import html2text
import logging

# Initialize the WebDriver
def initialize_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    logging.info("WebDriver initialized")
    return driver

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

# Main function to scrape URL and save content as Markdown
def scrape_url_to_markdown(url):
    driver = initialize_webdriver()

    try:
        
        driver.get(url)
        # time.sleep(2)  # Adjust based on the page's behavior
        base_url = extract_base_url(url)

        logging.info(f"Started processing URL: {url}")

        content = driver.find_element(
            By.TAG_NAME, 'body').get_attribute('outerHTML')
        markdown_content = convert_html_to_markdown(content, base_url)

        logging.info(
            f"Successfully processed URL: {url}")
        return markdown_content

    except Exception as e:
        logging.error(f"Error processing URL {url}: {str(e)}")
        return None
    
    finally:
        driver.quit()