'''Module containing all parsing scripts related to BeautifulSoup objects.'''

import requests
import json
from requests.models import Response
from bs4 import BeautifulSoup, Tag, Script

from .strings import replaceMultipleStrings

# class LetterboxdList:
#   pass

# insert a class object here for easier compact use
def getFilmId(tag: Tag) -> str | None:
  try:
    print(tag, 'TAG')
    _target = tag.find('div' 'film-watch-link-target')
    print(_target)
    return _target['data-film-id']
  except Exception as e:
    print(f"Error occurred while parsing film ID: {e}")
    return None

def getRankPlacement(tag: Tag) -> str:
  rank = int(tag.find('p', 'list-number').get_text())
  return rank

def getExtraPages(soup: BeautifulSoup) -> list:
  try:
      pagination_div = soup.find('div', 'paginate-pages')
      if pagination_div:
          extra_pages = [page_link.find('a')['href'] for page_link in pagination_div.ul.find_all('li') if page_link.find('a')]
          return extra_pages
      else:
          return []
  except Exception as e:
      print(f"Error occurred while parsing extra pages: {e}")
      return []

def getFilmName(film_poster: Tag) -> str:
  try:
    img_el = film_poster.find('img')
    if img_el:
      return img_el['alt']
    else:
      return film_poster['data-film-slug'].replace("-", ' ').title()
  except Exception as e:
    print(f"Error occurred while parsing film name: {e}")
    return ""

class LetterboxdFilmPage:
  """
  The Letterboxd film page handles a lazy-loaded DOM when scraped using BeautifulSoup
  This is different from the DOM shown on inspecting the page via browser.

  The data parsed here pertains to the content seen at the topmost portion
  of the page, from the film title to the runtime. It does not cover
  friend activity or reviews.

  Attributes
  ----------
  filmHeader: bs4.Tag
    the film's header element of the Soup object
  filmBody: bs4.Tag
    the film's content element of the Soup object
  filmFooter: bs4.Tag
    the film's footer element of the Soup object

  Methods
  ----------
  getFilmTitle():
    obtains film title
  getReleaseYear():
    obtains film release year
  getCastData():
    obtains film cast data
  getCrewData():
    obtains crew data
  getGenre():
    obtains film genre/s
  getRuntime():
    obtains film runtime
  """

  def __init__(self, soup: BeautifulSoup):
    self.filmHeader = soup.find('section', id='featured-film-header')
    self.filmBody = soup.find('div', id='tabbed-content')
    self.filmFooter = soup.find('p', ['text-link', 'text-footer'])
    self.contentNav = soup.find('div', id='content-nav')

    self.getScript(soup)
    # TODO: explore instantiating metadata on initialization
  
  def getScript(self, soup):
    scriptContent = soup.find('script', type='application/ld+json')

    # print(soup.find('script'))

    script = scriptContent.text.split('*/')[1].split('/*')[0]
    self.script = json.loads(script)

  def getRating(self) -> int|float | None:
    try:
      # handle error IF aggregate rating is not found
      json_script = self.script
      aggregateRating = json_script['aggregateRating']
      ratingValue = aggregateRating['ratingValue']
      return ratingValue
    except Exception as e:
      print(f"Error occurred while parsing film title: {e}")
      return None

  def getFilmTitle(self: Tag) -> str:
    try:
      return self.filmHeader.find('h1').get_text()
    
    except Exception as e:
      print(f"Error occurred while parsing film title: {e}")
      return ''
  
  def getProductionCompany(self: Tag) -> list[str]:
    try:
      return list(map(lambda x: x['name'], self.script['productionCompany']))
    except Exception as e:
      print(f"Error occurred while parsing production company: {e}")
      return None
  
  def getReleaseYear(self: Tag) -> int:
    try:
      return int(self.filmHeader.find('small', 'number').get_text())
    
    except Exception as e:
      print(f"Error occurred while parsing release year: {e}")
      return ''

  def getCastData(self: Tag) -> list[str]:
    try:
      cast_list = self.filmBody.find('div', 'cast-list').p
      cast  = [cast.text for cast in cast_list.find_all('a', 'text-slug') if cast.text.strip() or cast.text.strip() != 'Show All…']
      return cast
    except Exception as e:
      print(f"Error occurred while parsing cast members: {e}")
      return ['']
  
  def getCrewData(self: Tag) -> dict:
    crew_ = {}
    crew_div = self.filmBody.find('div', '-crewroles')
    if crew_div:
      crewroles = crew_div.find_all('h3')
      for role in crewroles:
        category = role.find('span', ['crewrole', '-full'])
        category_text = category.text
        category_sibling = role.find_next_sibling('div')
        if category_sibling:
          role_owners = [role_owner.get_text().strip() for role_owner in category_sibling.p if role_owner.text.strip()]
          crew_[category_text] = role_owners
        else:
          crew_[category_text] = None
    return crew_

  def getGenre(self: Tag) -> list[str]:
    try:
      genres_tab = self.filmBody.find('div', {'id':'tab-genres'})
      genres_list = genres_tab.find_all('a', 'text-slug')
      genres_ = [genre.get_text().strip() for genre in genres_list]
      return genres_
    except Exception as e:
      print(f"Error occurred while parsing genre: {e}")
      return ['']
  
  def getRuntime(self: Tag) -> int | None:
    try:
      genre_text = [replaceMultipleStrings(char) for char in self.filmFooter.stripped_strings]
      assert 'mins' in genre_text[0]
      mins_str = genre_text[0]
      mins_ = int(genre_text[0][:mins_str.index('mins')])
      return mins_
      # return genre_text[mins_ - 1]
    except Exception as e:
      print(f"Error occurred while parsing runtime: {e}")
      return None