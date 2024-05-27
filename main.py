import os
import json
from typing import Annotated, Any
from fastapi import FastAPI, Request, Body
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

import requests
import uuid
from pymongo.errors import ConnectionFailure
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime, timezone
from bson import Binary, decode

from obj.list import LetterboxdList
from obj.movie import LetterboxdFilmPage

from scripts.index import getRankPlacement, getExtraPages
from scripts.utils import strip_tz, convert_to_serializable

from dbconnect import connect_server, query_db, update_db

# Saved app variable will be run in the shell script
app = FastAPI()
origins = [
  "https://localhost:3000",
  "http://localhost:3000"
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
async def add(request: Request, status_code=300):
  redirect_url = request.url_for('scrape_letterboxd_list', list_slug='top-250-narrative-feature-length-filipino')
  return RedirectResponse(redirect_url)

@app.get(
    '/letterboxd-list/{list_slug}',
    tags=['letterboxd-list'],
    summary="Scrape and Fetch Letterboxd List"
  )
async def scrape_letterboxd_list(
  list_slug: str,
  parse_extra_pages: bool = True,
  film_parse_limit: int = None,
  save_scrape: bool = False
):
  '''
    Performs a webscraping function to extract data from lazy-loaded DOM
    in Letterboxd.
  '''

  history_id = uuid.uuid4()
  created_at = strip_tz(datetime.now(timezone.utc))
  page = requests.get(lboxd_list_link)
  soup = BeautifulSoup(page.content, 'lxml')

  list_object = LetterboxdList(soup)
  list_name = list_object.list_name
  publish_date = list_object.publish_date
  last_update = list_object.last_update
  total_pages = list_object.total_pages
  pages = getExtraPages(soup)
  results = soup.find_all('li', 'poster-container', limit=film_parse_limit)

  client = await connect_server()
  list_entry = await parse_list(lboxd_list_id, client)
  list_entry_date = list_entry['last_update']
  if list_entry_date == last_update:
    return jsonable_encoder(list_entry)

  films = []
  
  for result in tqdm(results):
    rank_placement = getRankPlacement(result)
    film_poster = result.find('div', 'film-poster')
    film_id = film_poster['data-film-id']
    film_slug = film_poster['data-film-slug']

    film = {
      'rank': rank_placement,
      'film_id': film_id,
    }

    query = { '_id': { '$eq': film_id } }
    film_in_db = await query_db(client, query, 'movie')
    # NOTE: explore adding additional flag to check if changes in movie were made
    if not film_in_db:
      print(f"New film detected in list! Parsing film_id: {film_id}")
      result = scrape_movie(film_slug, film_id)
      film_data = result['data']
      
      await update_db(client, film_data, 'movie')
    films.append(film)

  if pages and parse_extra_pages:
    for page in pages:
      html_page = requests.get(lboxd_url + page)
      soup = BeautifulSoup(html_page.content, 'lxml')
      results = soup.find_all('li', 'poster-container', limit=film_parse_limit)
      for result in tqdm(results):
        rank_placement = getRankPlacement(result)
        film_poster = result.find('div', 'film-poster')
        film_id = film_poster['data-film-id']
        film_slug = film_poster['data-film-slug']

        film = {
          'rank': rank_placement,
          'film_id': film_id,
        }

        query = { '_id': { '$eq': film_id } }
        film_in_db = await query_db(client, query, 'movie')
        if not film_in_db:
          print(f"New film detected in list! Parsing film_id: {film_id}")
          response = requests.get(lboxd_url + film_poster['data-target-link'])
          soup = BeautifulSoup(response.content, 'lxml')
          page = LetterboxdFilmPage(soup)
          film_data = page.getAllStats()
          new_film = {
            'film_id': film_id,
            **film_data
          }
          # NOTE: study validation of models before parsing
          page.validate_model(new_film) 
          
          await update_db(client, new_film, 'movie')

        films.append(film)
  
  list_history = {
    "_id": history_id,
    "list_id": lboxd_list_id,
    "list_name": list_name,
    "total_pages": total_pages,
    "data": films, 
    "publish_date": publish_date,
    "last_update": last_update,
    "created_at": created_at
  }

  if save_scrape:
    save_list = {
      "_id": Binary.from_uuid(history_id),
      "list_id": lboxd_list_id,
      "list_name": list_name,
      "total_pages": total_pages,
      "data": films,
      "publish_date": publish_date,
      "last_update": last_update,
      "created_at": created_at
    }
    await update_db(client, save_list, 'list_history')
  client.close()

  return list_history

@app.get('/movie/fetch/{id}', tags=['movie'], summary="Fetch movie in db")
async def fetch_movie(id: int | str, client: Any | None):
  try:
    client.admin.command('ping')
  except Exception:
    client = await connect_server()
  query = { '_id': { '$eq': str(id) }}
  movie_data = await query_db(client, query, 'movie')
  return movie_data[0]

@app.get(
    '/movie/scrape/{film_slug}', 
    tags=['movie'], 
    summary="Scrape movie from list"
  )
def scrape_movie(
  film_slug: str,
  film_id: Annotated[int, Body(embed=True)] = None
  ):
  film_base_uri = f"https://letterboxd.com/film/{film_slug}"
  response = requests.get(film_base_uri)
  soup = BeautifulSoup(response.content, 'lxml')
  page = LetterboxdFilmPage(soup)
  film_data = page.getAllStats()
  film = {
    **film_data
  }
  if film_id:
    film = {
      '_id': str(film_id),
      **film
    }
  page.validate_model(film)
  return { 'data': film }

@app.patch('/movie/{film_slug}', response_model=None, tags=['movie'], summary="Patch existing film from DB")
def update_movie(film_slug: str):
  # TODO: update movie metadata here
  return 

@app.get('/list-history', tags=['letterboxd-list'], summary="Fetch stored list-history item")
async def parse_list(id: int, client: Any | None = None, fetch_movies: bool = False):
  try:
    client.admin.command('ping')
  except Exception:
    client = await connect_server()
  query = { 'list_id': { '$eq': str(id) } }
  list_history = await query_db(client, query, 'list_history', 1)
  results = convert_to_serializable(list_history[0])
  
  if fetch_movies:
    data = results['data']
    tasks = [
      show_full_data(film, client) for film in data
    ]
    updated_films = await asyncio.gather(*tasks)
    results = updated_films
  return results

async def show_full_data(film, client):
  film_data = await fetch_movie(film['film_id'], client)
  try:
    del film_data['_id']
  except KeyError:
    pass
  updated_film = {
    **film,
    **film_data
  }
  return updated_film