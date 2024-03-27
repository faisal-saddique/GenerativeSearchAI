import streamlit as st
from utils.weaviate_utils import query_weaviate
import re
from utils.get_class_names_weaviate import get_class_names_weaviate
from utils.get_openai_response import get_openai_response

# Define a placeholder image URL
placeholder_image_url = "https://www.svgrepo.com/show/508699/landscape-placeholder.svg"

# Set up the Streamlit app title and sidebar
st.sidebar.title("Class Selection")
st.title("Generative AI Search")

# Function to fetch and update class names in session state
def fetch_and_update_class_names():
    st.session_state.class_names = get_class_names_weaviate()

# Check if class_names already exists in session state, if not fetch and update
if 'class_names' not in st.session_state:
    fetch_and_update_class_names()

# Button to refresh the fetching of class names
if st.sidebar.button("Refresh Class Names"):
    fetch_and_update_class_names()

# Retrieve available classes from Weaviate and store the selected class in session state
selected_class = st.sidebar.selectbox("Select a class", st.session_state.class_names)
st.session_state.selected_class = selected_class

# Check if selected_class is None or empty, and halt execution if true
if not st.session_state.selected_class:
    st.warning("Please select a class and ensure there are enough classes to select from your weaviate in order to proceed.")
    st.stop()

# Create an input text field for the user's query
user_query = st.text_input("Enter your search query", "")

# Slider for selecting the value of top_k
top_k = st.sidebar.slider("Select the number of results to retrieve", min_value=1, max_value=20, value=5)

# Perform search when the button is clicked or enter is pressed
if st.button("Search") or user_query:
    # Call the query_weaviate function to get search results
    results = query_weaviate(query=user_query, top_k=top_k, selected_class=st.session_state.selected_class)

    # Display search results
    with st.expander("Search Results"):
        for i, doc in enumerate(results, start=1):
            st.subheader(f"Result {i}")
            st.write("---")
            # Extract image URLs from markdown content using regex
            image_urls = re.findall(r'!\[.*?\]\((.*?)\)', doc.page_content)
            image_url = image_urls[0] if image_urls else placeholder_image_url

            # Create two columns for displaying image and text content
            col1, col2 = st.columns(2)

            with col1:
                # Display the image or placeholder
                st.image(image_url, caption=f"Image from result {i}")

            with col2:
                # Remove markdown image links from text content
                text_without_images = re.sub(r'!\[.*?\]\(.*?\)', '', doc.page_content)
                st.markdown(text_without_images)
                
            # Display metadata in JSON format
            st.markdown(f"**Source**: {doc.metadata['gsc_source_url']}")
            st.write("---")
        
    # Display response from OpenAI
    st.subheader("Results")
    placeholder = st.empty()
    # Pass search results and query to get_openai_response function
    get_openai_response(placeholder=placeholder, search_results=[doc.page_content for doc in results], query=user_query)