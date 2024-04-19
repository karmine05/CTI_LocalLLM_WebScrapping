import ollama
import json
import bs4
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import tqdm

while True:
    url = input("Please enter the DFIR Report URL or enter 'quit' to complete the task: ")
    if url.lower() == 'quit':
        break # Break out of the loop and end the chat
    else:
        loader = WebBaseLoader(
            web_paths=(url,),
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    class_=("entry-content", "entry-title", "entry-header")
                )
            ),
        )
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        with open('dfir_raw.txt', 'a', encoding="utf-8") as f:
            for split in tqdm.tqdm(splits, desc="Ingestion progress"):
                f.write(str(split))
            f.write("\n")  # Move the newline here