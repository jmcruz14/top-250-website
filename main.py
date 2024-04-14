from fastapi import FastAPI
# import asyncio
import requests
from bs4 import BeautifulSoup
# import polars as pl
from tqdm import tqdm

# TODO: serve data thru fastapi -> fetch into vue app on load in router

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait

# from scrape_lboxd import scrapeSoup
from scripts.main import getExtraPages, getFilmName, getFilmPageContent, getCastData, getCrewData

# Saved app variable will be run in the shell script
app = FastAPI()
lboxd_url = 'https://letterboxd.com'
lboxd_list_link = 'https://letterboxd.com/tuesjays/list/top-250-narrative-feature-length-filipino/'

@app.get("/")
async def root():

  # Read URL here
  # Run the scraping algorithm in a separate file
  page = requests.get(lboxd_list_link)
  soup = BeautifulSoup(page.content, 'html.parser')
  pages = getExtraPages(soup)
  
  results = soup.find_all('li', 'poster-container', limit=1)

  films = []
  for result in tqdm(results):
    rank_placement = result.find('p', 'list-number').get_text()
    film_poster = result.find('div', 'film-poster')
    
    name = getFilmName(film_poster)
    film_metadata_results = getFilmPageContent(lboxd_url + film_poster['data-target-link'])
    cast_list = getCastData(film_metadata_results)
    crew_ = getCrewData(film_metadata_results)
  #   # TODO: extract other metadata
    films.append({
      'film': name,
      'rank': rank_placement,
      'cast': cast_list,
      **crew_
    })

  # data = scrapeSoup(films)
  # print(data)

  return {
    "message": "Hello World",
    "pagecontent": films
  }