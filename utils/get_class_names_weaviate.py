import weaviate
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

@st.cache_data(ttl="1h")
def get_class_names_weaviate():
    WEAVIATE_URL = os.getenv("WEAVIATE_URL")
    auth_client_secret = weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY"))

    client = weaviate.Client(
        url=WEAVIATE_URL,
        additional_headers={
            "X-Openai-Api-Key": os.getenv("OPENAI_API_KEY"),
        },
        auth_client_secret=auth_client_secret
    )

    return [cls['class'] for cls in client.schema.get()['classes']]

