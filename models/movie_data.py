from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
  film_id: str | None = Field(
    default=None,
    title="film numerical id extracted from parent list",
    examples=["111490"]
    )
  film_slug: str | None = Field(
    default=None,
    title="film_title denoted in snake_case form",
    examples=["v-for-vendetta"]
  )
  film_title: str | None = Field(
    default=None,
    title="film title without any string manipulations"
  )
  year: Optional[int] = None
  rating: Optional[float] = None
  classic_rating: Optional[float] = None
  review_count: Optional[int] = None
  rating_count: Optional[int] = None
  watch_count: Optional[int] = None
  list_appearance_count: Optional[int] = None
  like_count: Optional[int] = None
  genre: Optional[list[str]] = None
  runtime: Optional[int] = None
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

