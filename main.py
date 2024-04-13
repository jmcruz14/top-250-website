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

from scrape_lboxd import scrapeSoup

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
  results = soup.find_all('li', 'poster-container', limit=1)

  films = []
  for result in tqdm(results):
    rank_placement = result.find('p', 'list-number').get_text()
    film_content = result.find('div', 'film-poster')
    
    film_page = requests.get(lboxd_url + film_content['data-target-link'])
    film_page_soup = BeautifulSoup(film_page.content, 'html.parser')
    film_metadata_results = film_page_soup.find('div', id='tabbed-content')
    cast_list = [cast.text for cast in film_metadata_results.find('div', 'cast-list').p if cast.text.strip()]
    # TODO: extract other metadata

    crew_div = film_metadata_results.find('div', '-crewroles')
    crew_ = {}
    crewroles = crew_div.find_all('h3')
    for role in crewroles:
      print(role)
      category = role.find('span', ['crewrole', '-full'])
      category_text = category.text
      category_sibling = role.find_next_sibling('div')
      if category_sibling:
        role_owners = [role_owner.get_text().strip() for role_owner in category_sibling.p if role_owner.text.strip()]
        crew_[category_text] = role_owners
      else:
        crew_[category_text] = None

    # print(film_metadata_results)
    print(film_metadata_results.find('div', '-crewroles').prettify())

    films.append({
      'film': film_content['data-film-slug'].replace("-", ' ').title(),
      'rank': rank_placement,
      'cast': cast_list,
      'crew': crew_
      # 'page_content': film_metadata_results.text
    })
  # results = soup.find_all('div', 'really-lazy-load')
  data = scrapeSoup(films)
  print(data)
  # print(type(films))

  return {
    "message": "Hello World",
    "pagecontent": films
  }