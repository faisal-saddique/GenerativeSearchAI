import streamlit as st
from utils.weaviate_utils import query_weaviate
import re

placeholder_image_url = "https://www.svgrepo.com/show/508699/landscape-placeholder.svg"  # Replace with your placeholder image URL

# Set up the Streamlit app title
st.title("Generative AI Search")

# Create an input text field for the user's query
user_query = st.text_input("Enter your search query", "")

if st.button("Search") or user_query:
    top_k = 5  # The number of results you want to retrieve

    # Call the query_weaviate function when the button is clicked or enter is pressed
    results = query_weaviate(query=user_query, top_k=top_k)

    # Loop through the results and display them in an expander
    st.subheader("Results")
    for i, doc in enumerate(results, start=1):
        st.write("---")
        # Use regex to find image URLs in markdown content
        image_urls = re.findall(r'!\[.*?\]\((.*?)\)', doc.page_content)
        image_url = image_urls[0] if image_urls else placeholder_image_url

        # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            # Display the image or the placeholder
            st.image(image_url, caption=f"Image from result {i}")

        with col2:
            # Display the text content without the markdown image link
            text_without_images = re.sub(r'!\[.*?\]\(.*?\)', '', doc.page_content)
            st.markdown(text_without_images)
        
        
        # Optionally, you can also display the metadata in JSON format
        st.markdown(f"**Source**: {doc.metadata['gsc_source_url']}")
        st.write("---")