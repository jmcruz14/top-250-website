'''Module containing all parsing scripts related to BeautifulSoup objects.'''

import requests
from requests.models import Response
from bs4 import BeautifulSoup, Tag

from .strings import replaceMultipleStrings

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
  
def getFilmPageContent(soup: BeautifulSoup) -> Tag:
  '''
  This function processes a request through the returned Response
  and returns a Tag object that contains the pertinent film metadata
  for further extraction.

  \n
  NOTE: The script handles a lazy-loaded DOM of the website, which is
  different from the DOM seen when inspecting the Letterboxd website.

  Parameters:
    response (requests.Response): Returned HTTP request response
  
  Returns:
    metadata (bs4.Tag): Tag object containing the selected page content
  '''
  metadata = soup.find('div', id='tabbed-content')
  return metadata

def getFilmPageFooter(soup: BeautifulSoup) -> Tag | None:
  footer = soup.find('p', ['text-link', 'text-footer'])
  return footer

def getCastData(metadata: Tag) -> list:
  cast = [cast.text for cast in metadata.find('div', 'cast-list').p if cast.text.strip()]
  return cast
  
def getCrewData(metadata: Tag) -> dict:
  crew_ = {}
  crew_div = metadata.find('div', '-crewroles')
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

def getGenre(soup: BeautifulSoup) -> list[str]:
  genres_tab = soup.find('div', {'id':'tab-genres'})
  genres_list = genres_tab.find_all('a', 'text-slug')
  genres_ = [genre.get_text().strip() for genre in genres_list]
  return genres_

def getRuntime(soup: BeautifulSoup) -> int | None:
  try:
    print(soup.text)
    # genre_text = soup.get_text().strip().replace('\n', '').split(' ')
    genre_text = [replaceMultipleStrings(char) for char in soup.stripped_strings]
    print(genre_text)
    assert 'mins' in genre_text[0]
    mins_str = genre_text[0]
    mins_ = int(genre_text[0][:mins_str.index('mins')])
    print(mins_)
    return mins_
    # return genre_text[mins_ - 1]
  except Exception as e:
    print(f"Error occurred while parsing runtime: {e}")
    return None