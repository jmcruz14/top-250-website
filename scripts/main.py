'''Module containing all parsing scripts related to BeautifulSoup objects.'''

import requests
from bs4 import BeautifulSoup, Tag

def getExtraPages(soup: BeautifulSoup) -> list:
  pagination_div = soup.find('div', 'paginate-pages')
  if pagination_div:
    extra_pages = [page_link.find('a')['href'] for page_link in pagination_div.ul.find_all('li') if page_link.find('a')]
    return extra_pages
  else:
    return []

def getFilmName(film_poster: Tag) -> str:
  img_el = film_poster.find('img')
  name = str()
  if img_el:
    name = img_el['alt']
  else:
    name = film_poster['data-film-slug'].replace("-", ' ').title()
  return name
  
def getFilmPageContent(url: str) -> Tag:
  '''
  This function processes a request through the passed URL
  and returns a Tag object that contains the pertinent film metadata
  for further extraction.

  \n
  NOTE: The script handles a lazy-loaded DOM of the website, which is
  different from the DOM seen when inspecting the Letterboxd website.
  '''

  film_page = requests.get(url)
  soup = BeautifulSoup(film_page.content, 'html.parser')
  metadata = soup.find('div', id='tabbed-content')
  return metadata

def getCastData(metadata: Tag) -> list:
  cast = [cast.text for cast in metadata.find('div', 'cast-list').p if cast.text.strip()]
  return cast
  
def getCrewData(metadata: Tag) -> object:
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