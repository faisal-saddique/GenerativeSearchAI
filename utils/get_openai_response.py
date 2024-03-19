from openai import OpenAI
from dotenv import load_dotenv
from utils.prompts import Prompts

load_dotenv()

client = OpenAI()

def get_openai_response(placeholder, search_results: list[str], query):
    system_prompt = Prompts.get_main_prompt(search_results=search_results,query=query)
    stream = client.chat.completions.create(
        messages=[{"role":"system","content":system_prompt}],
        model="gpt-4-1106-preview",
        stream=True
    )
    streamed_text = ""
    for chunk in stream:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content is not None:
            streamed_text = streamed_text + chunk_content
            placeholder.write(streamed_text)