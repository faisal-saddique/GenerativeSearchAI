
# GenerativeSearchAI

GenerativeSearchAI is a system designed to scrape web content, convert it to markdown, and index it for easy retrieval using generative AI techniques. It leverages the power of Weaviate, an AI-powered database, to store and search through the indexed content.

## Features

- Scrape web content and convert it to markdown format.
- Split text into manageable chunks for better indexing.
- Index content in Weaviate for AI-powered search capabilities.
- Provide a user interface for searching indexed content.

## Installation

To install GenerativeSearchAI, you need to have Python installed on your system. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/faisal-saddique/GenerativeSearchAI.git
cd GenerativeSearchAI
pip install -r requirements.txt
```

## Usage

To start using GenerativeSearchAI, follow these steps:

1. Set up your environment variables by creating a `.env` file with the following keys:
   - `WEAVIATE_URL`: The URL to your Weaviate instance.
   - `WEAVIATE_API_KEY`: Your Weaviate API key.
   - `OPENAI_API_KEY`: Your OpenAI API key.

2. Run the main script to scrape content and index it:

```python
python main.py
```

3. Start the Streamlit app to use the search interface:

```bash
streamlit run app.py
```

## Acknowledgements

- [Weaviate](https://weaviate.io/)
- [Streamlit](https://streamlit.io/)
- [Selenium](https://www.selenium.dev/)
- [Langchain](https://langchain.dev/)