import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

import requests
import uuid
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime, timezone

from obj.list import LetterboxdList
from obj.movie import LetterboxdFilmPage

from scripts.index import getRankPlacement, getExtraPages
from scripts.utils import strip_tz

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
lboxd_list_id = '15294077'

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
  print(f"{repr(exc)}")
  return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# Return a Redirect Response for modification
# FastAPI is a subclass of Starlette
@app.get('/')
async def add(request: Request):
  redirect_url = request.url_for('root')
  return RedirectResponse(redirect_url)

@app.get('/movie/{film_slug}', tags=['movie'], summary="Fetch movie from db")
def fetch_movie(film_slug: str):
  # TODO: return movie entry here
  return { 'movie-to-scrape': film_slug }

@app.patch('/movie/{film_slug}', response_model=None, tags=['movie'], summary="Patch existing film from DB")
def update_movie(film_slug: str):
  # TODO: update movie metadata here
  return 
# FastAPI is by default, returning a JSONResponse object
@app.get("/main")
async def root():
  """
    This is the main API call function which performs a GET request of the Letterboxd data
    currently present here.
  """

  history_id = uuid.uuid4()
  created_at = strip_tz(datetime.now(timezone.utc))

  # Read URL here
  # Run the scraping algorithm in a separate file
  # lxml > html.parser in terms of performance
  page = requests.get(lboxd_list_link)
  soup = BeautifulSoup(page.content, 'lxml')

  list_object = LetterboxdList(soup)
  list_name = list_object.list_name
  publish_date = list_object.publish_date
  last_update = list_object.last_update
  total_pages = list_object.total_pages

  # FLAGS
  get_stats_data = False
  get_extra_pages = False
  page_limit = 1
  # page_limit = None

  # list_text = soup
  pages = getExtraPages(soup)
  results = soup.find_all('li', 'poster-container', limit=page_limit)

  films = []
  
  # Change this to: GET MOVIE IF ENABLED
  for result in tqdm(results):
    rank_placement = getRankPlacement(result)
    film_poster = result.find('div', 'film-poster')
    id_ = film_poster['data-film-id']

    film = {
      'rank': rank_placement,
      'id_': id_,
      # 'content': page.script,
    }

    # update flag to: if film_id is not found in the repo
    if get_stats_data:
      response = requests.get(lboxd_url + film_poster['data-target-link'])
      soup = BeautifulSoup(response.content, 'lxml')
      page = LetterboxdFilmPage(soup)
      film_data = page.getAllStats()

      film = {
        **film,
        **film_data
      }
    
    # page.validate_model(film)

    films.append(film)

  if pages and get_extra_pages:
    print(pages, 'page-count')
    for page in pages:
      html_page = requests.get(lboxd_url + page)
      soup = BeautifulSoup(html_page.content, 'lxml')
      results = soup.find_all('li', 'poster-container')
      for result in tqdm(results):
        rank_placement = getRankPlacement(result)
        film_poster = result.find('div', 'film-poster')
        id_ = film_poster['data-film-id']

        film = {
          'rank': rank_placement,
          'id_': id_,
          # 'content': page.script,
        }

        if get_stats_data:
          response = requests.get(lboxd_url + film_poster['data-target-link'])
          soup = BeautifulSoup(response.content, 'lxml')
          page = LetterboxdFilmPage(soup)
          film_data = page.getAllStats()

          film = {
            **film,
            **film_data
          }
        films.append(film)

  return {
    "id_": history_id,
    "list_id": lboxd_list_id,
    "list_name": list_name,
    "total_pages": total_pages,
    "data": films,
    "publish_date": publish_date,
    "last_update": last_update,
    "created_at": created_at
    # "content": str(list_text)
  }