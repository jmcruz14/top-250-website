def test_mongodb_fixture(mongodb):
  """ This test will pass if MDB_URI is set to a valid connection string. """
  assert mongodb.admin.command("ping")["ok"] > 0

def test_query_db_list_history(mongodb, rollback_session):
  documents = mongodb.letterboxd_list.list_history.find({}, session=rollback_session)
  obj = [doc for doc in documents]

  assert documents is not None
  assert len(obj) >= 1

def test_query_db_movie(mongodb, rollback_session):
  query = {
    "director": "Lav Diaz"
  }
  documents = mongodb.letterboxd_list.movie.find(query, session=rollback_session)
  obj = [doc for doc in documents]

  assert documents is not None
  assert len(obj) >= 1