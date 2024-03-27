import streamlit as st

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Generative AI Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Downloaded Sitemaps")

if "downloaded_sitemaps" in st.session_state:
    for filename, sitemap_data in st.session_state["downloaded_sitemaps"].items():
        with st.expander(f"Sitemap: {filename}"):
            st.text(sitemap_data['xml_content'])
else:
    st.write("No history")