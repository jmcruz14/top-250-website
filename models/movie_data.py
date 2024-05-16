from pydantic import BaseModel
from typing import Optional

class Movie(BaseModel):
  film_id: str
  film_slug: str
  film_title: str
  year: int
  rating: Optional[float] = None
  classic_rating: Optional[float] = None
  review_count: int
  rating_count: int
  watch_count: int
  list_appearance_count: int
  like_count: int
  genre: Optional[list[str]] = None
  runtime: int
  cast: Optional[list[str]] = None
  production_company: Optional[list[str]] = None
  director: Optional[list[str]] = None
  writer: Optional[list[str]] = None
  editor: Optional[list[str]] = None
  cinematography: Optional[list[str]] = None
  assistant_director: Optional[list[str]] = None
  production_design: Optional[list[str]] = None
  art_direction: Optional[list[str]] = None
  sound: Optional[list[str]] = None
  # poster: Optional[str] = None

