
import json
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
# import asyncio
import requests
from bs4 import BeautifulSoup, Script, CData
import polars as pl
from tqdm import tqdm

# TODO: serve data thru fastapi -> fetch into vue app on load in router

# from scrape_lboxd import scrapeSoup
from scripts.index import getExtraPages, getRankPlacement, getFilmId, LetterboxdFilmPage

# Saved app variable will be run in the shell script
app = FastAPI()
origins = [
  "https://localhost:3000"
]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

lboxd_url = 'https://letterboxd.com'
lboxd_list_link = 'https://letterboxd.com/tuesjays/list/top-250-narrative-feature-length-filipino/'

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
  print(f"{repr(exc)}")
  return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# @app.

# Return a Redirect Response for modification
# FastAPI is a subclass of Starlette
@app.get('/')
async def add(request: Request):
  redirect_url = request.url_for('root')
  return RedirectResponse(redirect_url)

# FastAPI is by default, returning a JSONResponse object
@app.get("/main")
async def root():
  """
    Root function is served when a get request is executed in the main address.
  """

  # Read URL here
  # Run the scraping algorithm in a separate file
  # lxml > html.parser
  page = requests.get(lboxd_list_link)
  soup = BeautifulSoup(page.content, 'lxml')
  pages = getExtraPages(soup)
  
  # lxml_soup = BeautifulSoup(page.content, 'lxml')
  # print(lxml_soup)

  results = soup.find_all('li', 'poster-container', limit=1)

  films = []
  for result in tqdm(results):
    rank_placement = getRankPlacement(result)
    film_poster = result.find('div', 'film-poster')
    id_ = film_poster['data-film-id']

    response = requests.get(lboxd_url + film_poster['data-target-link'])
    soup = BeautifulSoup(response.content, 'lxml')

    page = LetterboxdFilmPage(soup)
    name = page.getFilmTitle()
    rating = page.getRating()
    release_year = page.getReleaseYear()
    cast = page.getCastData()
    crew_ = page.getCrewData()
    production_company = page.getProductionCompany()
    genre_ = page.getGenre()
    runtime_ = page.getRuntime()
    
    films.append({
      'id': id_,
      'film': name,
      'year': release_year,
      'rank': rank_placement,
      'rating': rating,
      'genre': genre_,
      'runtime': runtime_,
      'cast': cast,
      'production_company': production_company,
      'content': page.script,
      **crew_,
    })
  
  # if pages:
  #   for page in pages:
  #     html_page = requests.get(lboxd_url + page)
  #     soup = BeautifulSoup(html_page.content, 'lxml')
  #     results = soup.find_all('li', 'poster-container')
  #     for result in tqdm(results):
  #       rank_placement = getRankPlacement(result)
  #       film_poster = result.find('div', 'film-poster')

  #       response = requests.get(lboxd_url + film_poster['data-target-link'])
  #       soup = BeautifulSoup(response.content, 'lxml')

  #       page = LetterboxdFilmPage(soup)
  #       name = page.getFilmTitle()
  #       rating = page.getRating()
  #       release_year = page.getReleaseYear()
  #       cast = page.getCastData()
  #       crew_ = page.getCrewData()
  #       production_company = page.getProductionCompany()
  #       genre_ = page.getGenre()
  #       runtime_ = page.getRuntime()
        
  #       films.append({
  #         'film': name,
  #         'year': release_year,
  #         'rank': rank_placement,
  #         'rating': rating,
  #         'genre': genre_,
  #         'runtime': runtime_,
  #         'cast': cast,
  #         'production_company': production_company,
  #         'content': page.script,
  #         **crew_,
  #       })


  # if pages:
  #   for page in pages:
  #     html_page = requests.get(lboxd_url + page)
  #     soup = BeautifulSoup(html_page.content, 'lxml')
  #     results = soup.find_all('li', 'poster-container')
  # data = scrapeSoup(films)
  # print(data)
  # if pages:
  #   for page in pages:
  #     html_page = requests.get(lboxd_url + page)
  #     soup = BeautifulSoup(html_page.content, 'lxml')
  #     results = soup.find_all('li', 'poster-container')
  #     for result in tqdm(results):
  #       rank_placement = result.find('p', 'list-number').get_text()
  #       film_poster = result.find('div', 'film-poster')
        
  #       name = getFilmName(film_poster)
  #       film_metadata_results = getFilmPageContent(lboxd_url + film_poster['data-target-link'])
  #       cast_list = getCastData(film_metadata_results)
  #       crew_ = getCrewData(film_metadata_results)
        
  #       # TODO: extract other metadata
  #       films.append({
  #         'rank': rank_placement,
  #         'film': name,
  #         'cast': cast_list,
  #         **crew_ 
  #       })
  
  # TODO: put in separate file for further flexibility
  # df = pl.DataFrame(films)
  # df.write_excel("top_250_saved_file.xlsx")

  # return df
  return {
    "results": films
  }