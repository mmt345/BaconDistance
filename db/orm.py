from sqlalchemy import Column, String, ForeignKey, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Actor(Base):
    """Represents an actor with a unique IMDb ID, and name."""
    __tablename__ = "actors"
    imdb_id = Column(String, primary_key=True, nullable=False) 
    name    = Column(String, nullable=False)

class Movie(Base):
    """Represents a movie with a unique IMDb ID, and title (meaning movie name)."""
    __tablename__ = "movies"
    imdb_id = Column(String, primary_key=True, nullable=False) 
    title   = Column(String, nullable=False)

class Cast(Base):
    """
    Represents a connection between actor and a movie where the actor is a castmate in the movie.

    You might ask yourself why `movie_imdb_id` and `actor_imdb_id` aren't foreign keys -> foreign keys are intentionally omitted because 
    the IMDb principals file references IDs that do not exist in the actors/movies files.
    I can filter those out but it makes `generate_db` much slower so this favors faster loads.
    """

    __tablename__ = "casts"
    movie_imdb_id = Column(String, primary_key=True)
    actor_imdb_id = Column(String, primary_key=True)
