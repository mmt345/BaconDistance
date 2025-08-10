from datetime import datetime
from typing import List, Dict, Set, Iterator
from download_imdb_data import download_all_imdb_datasets
from db_session import engine, local_session, Session
from orm import Base, Actor, Movie, Cast

# CONFIGURATION
ACTORS_PATH = 'name.basics.tsv'
CAST_PATH = 'title.principals.tsv' # This holds the relationships between actors and movies according to imdb_ids
MOVIES_PATH = 'title.basics.tsv'

MAX_ACTORS = 10000000
MAX_CAST = 20000000
MAX_MOVIES = 10000000

# TSV FIELD COUNTS
ACTOR_NUM_FIELDS = 6
CAST_NUM_FIELDS = 6
MOVIE_NUM_FIELDS = 9

def create_schema() -> None:
    """
    Drops all existing ORM tables and recreates the schema.
    """
    print("Dropping all tables")
    Base.metadata.drop_all(engine)
    print("Creating all tables")
    Base.metadata.create_all(engine)


def read_tsv_lines(file_path: str, max_rows: int) -> Iterator[List[str]]:
    """
    Reads a TSV file, skips the header, and yields up to max_rows split lines.
    Each line is split into parts using tab.

    :param file_path: Path to the TSV file.
    :param max_rows: Maximum number of lines to read.
    :yields: The fields of each TSV line as a list of strings (split parts).
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        next(f)  # Skip header

        for i, line in enumerate(f):
            if i <= max_rows:
                yield line.strip().split('\t')

# LOADERS
def load_actors(session: Session, file_path: str, max_rows: int) -> Set[str]:
    """
    Loads actors from IMDb's name.basics.tsv file and commits them to the db.

    :param session: Active SQLAlchemy session.
    :param file_path: Path to the name.basics.tsv file.
    :param max_rows: Max number of rows to read.
    :return: Set of actor IMDb IDs that were inserted to the db.
    """
    actor_imdb_ids: Set[str] = set()

    for i, parts in enumerate(read_tsv_lines(file_path, max_rows)):
        if len(parts) == ACTOR_NUM_FIELDS:
            imdb_id, name, _, _, professions_str, _ = parts
            professions = professions_str.split(',')

            if any(prof in professions for prof in ("actor", "actress")):
                actor = Actor(imdb_id=imdb_id, name=name)
                session.add(actor)
                actor_imdb_ids.add(imdb_id)
            if i % 10000 == 0:
                session.commit()
        else:
            print(f"Line number {i} in actors table doesn't match the required number of fields {ACTOR_NUM_FIELDS}.")

    session.commit()
    return actor_imdb_ids

def load_cast(
    session: Session,
    file_path: str,
    max_rows: int
) -> Dict[str, Set[str]]:
    """
    Loads movie-to-actor relationships from IMDb's title.principals.tsv file and commits them to the db.

    :param session: Active SQLAlchemy session.
    :param file_path: Path to the title.principals.tsv file.
    :param max_rows: Max number of rows to read.
    :return: A dictionary mapping movie IMDb IDs to a set of actor IMDB IDs.
    """
    casts = {}

    for i, parts in enumerate(read_tsv_lines(file_path, max_rows)):
        if len(parts) == CAST_NUM_FIELDS:
            movie_imdb_id, _, actor_imdb_id, category, _, _ = parts

            if category in {"actor", "actress"}:
                casts.setdefault(movie_imdb_id, set()).add(actor_imdb_id)
        else:
            print(f"Line number {i} in cast table doesn't match the required number of fields {CAST_NUM_FIELDS}.")

    print(f"Found {len(casts)} casts")
    for i, (movie_id, actor_ids) in enumerate(casts.items()):
        for actor_id in actor_ids:
            session.add(Cast(movie_imdb_id=movie_id, actor_imdb_id=actor_id))
        if i % 10000 == 0:
            session.commit()

    session.commit()
    return casts

def load_movies(
    session: Session,
    file_path: str,
    max_rows: int
) -> Set[str]:
    """
    Loads movies from IMDb's title.basics.tsv file and commits them to the db.

    :param session: Active SQLAlchemy session.
    :param file_path: Path to the title.basics.tsv file.
    :param max_rows: Max number of rows to read.
    :return: Set of movie IMDb IDs that were inserted to the db.
    """
    movie_imdb_ids: Set[str] = set()

    for i, parts in enumerate(read_tsv_lines(file_path, max_rows)):
        if len(parts) == MOVIE_NUM_FIELDS:
            imdb_id, title_type, title, _, _, _, _, _, _ = parts

            if title_type == "movie":
                movie = Movie(imdb_id=imdb_id, title=title)
                session.add(movie)
                movie_imdb_ids.add(imdb_id)
            if i % 10000 == 0:
                session.commit()
        else:
            print(f"Line number {i} in movies table doesn't match the required number of fields {MOVIE_NUM_FIELDS}.")

    session.commit()
    return movie_imdb_ids


def main() -> None:
    download_all_imdb_datasets()
    create_schema()

    with local_session() as session:
        print(f"{datetime.now().strftime('%H:%M:%S')} Loading actors...")
        actors = load_actors(session, ACTORS_PATH, max_rows=MAX_ACTORS)
        print(f"{datetime.now().strftime('%H:%M:%S')} Loaded {len(actors)} actors.")

        print(f"{datetime.now().strftime('%H:%M:%S')} Loading movies...")
        movies = load_movies(session, MOVIES_PATH, max_rows=MAX_MOVIES)
        print(f"{datetime.now().strftime('%H:%M:%S')} Loaded {len(movies)} movies.")

        print(f"{datetime.now().strftime('%H:%M:%S')} Loading cast...")
        castmates = load_cast(session, CAST_PATH, max_rows=MAX_CAST)
        print(f"{datetime.now().strftime('%H:%M:%S')} Loaded {len(castmates)} castmates.")

    print(f"{datetime.now().strftime('%H:%M:%S')} Done.")


if __name__ == "__main__":
    main()
