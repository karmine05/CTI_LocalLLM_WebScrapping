import requests
import bs4
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.runnables import RunnablePassthrough
import tqdm

def scrape_dfir_report(url):
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
    dfir_content = ""
    for split in tqdm.tqdm(splits, desc="Ingestion progress"):
        dfir_content += str(split)
    dfir_content += "\n"
    return dfir_content

def scrape_hacker_news(url):
    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("content section", "articlebody", "story-title")
            )
        ),
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    hn_content = ""
    for split in tqdm.tqdm(splits, desc="Ingestion progress"):
        hn_content += str(split)
    hn_content += "\n"
    return hn_content

def scrape_bleeping_computer(url):
    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("article_section", "articleBody")
            )
        ),
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    bc_content = ""
    for split in tqdm.tqdm(splits, desc="Ingestion progress"):
        bc_content += str(split)
    bc_content += "\n"
    return bc_content

def save_to_txt(content, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content)

if __name__ == "__main__":
    while True:
        option = input("Please choose an option:\n1. Scrape DFIR Report\n2. Scrape Hacker News\n3. Scrape BleepingComputer\nEnter 'quit' to complete the task: ")
        
        if option == 'quit':
            break
        
        url = input("Please enter the URL: ")
        
        if option == '1':
            # Scrape DFIR Report
            blog_content = scrape_dfir_report(url)
        elif option == '2':
            # Scrape Hacker News
            blog_content = scrape_hacker_news(url)
        elif option == '3':
            # Scrape BleepingComputer
            blog_content = scrape_bleeping_computer(url)
        else:
            print("Invalid option. Please choose either 1, 2, or 3")
            continue
        
        # Save the content to a common file
        if blog_content:
            save_to_txt(blog_content, 'blog_post.txt')
            print("Blog content appended to 'blog_post.txt'")
        else:
            print("Failed to scrape blog content!")
