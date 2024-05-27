from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from models.movie_data import Movie

class ListHistory(BaseModel):
  history_id: UUID
  list_name: str
  total_pages: int
  data: list[Movie]
  last_update: datetime
  createdAt: datetime
