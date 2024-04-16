import json
import requests
import re
from bs4 import BeautifulSoup, Tag

from .strings import not_numeric, replaceMultipleStrings
# from .url import fetchStatsUrl

from constants.url import fetchStatsUrl

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
    # print(soup)

    self.getScript(soup)
    self.film_id = self.script['url'].split('/')[4]
    self.getStats(self.film_id)
    self.getReviewCount()
    self.getRatingCount()
    # TODO: explore instantiating metadata on initialization
  
  def getScript(self, soup):
    scriptContent = soup.find('script', type='application/ld+json')
    script = scriptContent.text.split('*/')[1].split('/*')[0]
    self.script = json.loads(script)
  
  def getStats(self, film_id: str):
    '''
      The stats data is retrieved from a different endpoint (/csi/film/{movie}/stats)
      before it is loaded onto the resulting page. 
    '''
    self.statsUrl = fetchStatsUrl(film_id)
    statsRequest = requests.get(self.statsUrl)
    statsSoup = BeautifulSoup(statsRequest.content, 'lxml')
    self.watchCount = int(re.sub(not_numeric, '', statsSoup.find('li', 'filmstat-watches').a.get('title')))
    self.listAppCount = int(re.sub(not_numeric, '', statsSoup.find('li', 'filmstat-lists').a.get('title')))
    self.likeCount = int(re.sub(not_numeric, '', statsSoup.find('li', 'filmstat-likes').a.get('title')))

  def getRating(self) -> int|float | None:
    try:
      # handle error IF aggregate rating is not found
      json_script = self.script
      if 'aggregateRating' in json_script:
        aggregateRating = json_script['aggregateRating']
        ratingValue = aggregateRating['ratingValue']
        return ratingValue
      else:
        # perform classic rating algorithm here?
        # or just keep it separate?
        raise Exception
    except Exception as e:
      print(f"Error occurred while parsing rating: {e}")
      return None
  
  def getReviewCount(self) -> None:
    try:
      json_script = self.script
      aggregateRating = json_script['aggregateRating']
      reviewCount = aggregateRating['reviewCount']
      self.reviewCount = reviewCount
    except Exception as e:
      print(f"Error occurred while parsing review count: {e}")
      self.reviewCount = None

  def getRatingCount(self) -> None:
    try:
      # handle error IF aggregate rating is not found
      json_script = self.script
      aggregateRating = json_script['aggregateRating']
      ratingCount = aggregateRating['ratingCount']
      self.ratingCount = ratingCount
    except Exception as e:
      print(f"Error occurred while parsing rating count: {e}")
      self.ratingCount = None

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

if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')