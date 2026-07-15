import streamlit as web
from Bio import Entrez
from datetime import datetime,timedelta
web.title("NCBI Academic Paper Search")
email = web.text_input ("add personal email (required by ncbi)", "Eilidh.McVie@childrens.harvard.edu")
query_term = web.text_input("add search query term", "traumatic brain injury")
number_of_results_desired = web.slider("Select Number of Results Desired", min_value=1, max_value=200, value=5)
today = datetime.now()
search_frame = web.slider("time period of search", min_value=1, max_value=365, value=14)
start_date = today - timedelta(days=int(search_frame))
fmt = '%Y/%m/%d'
date_str = f"{start_date.strftime(fmt)}:{today.strftime(fmt)}"
print(f"Searching for articles from: {date_str}")
Entrez.email = {email}
query_term = {query_term}
def search_and_fetch_pubmed(query_term):
    results = []
    with Entrez.esearch(db="pubmed", term=query_term, mindate=start_date.strftime(fmt),
    maxdate=today.strftime(fmt), datetype="pdat", retmax=number_of_results_desired) as item:
        search_results = Entrez.read(item) 
    id_list = search_results["IdList"]

    if not id_list:
        print("No results found")
        return
    with Entrez.efetch(db="pubmed", id=id_list, rettype="abstract", retmode="xml") as item:
        records = Entrez.read(item)
    for article in records["PubmedArticle"]:
        medline_citation = article["MedlineCitation"]
        pmid = medline_citation["PMID"]
        title = medline_citation["Article"]["ArticleTitle"]
        results.append(f"**PMID:** {pmid}\nTitle: {title}")
    for result in results:
        web.write(result)
if web.button("Search"):
    search_and_fetch_pubmed(query_term)
