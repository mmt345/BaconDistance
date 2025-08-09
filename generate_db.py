import orjson
from datetime import datetime
from typing import List, Dict, Tuple
from actor import Actor
from movie import Movie
from download_imdb_data import download_all_imdb_datasets

# CONFIGURATION
ACTORS_PATH = 'name.basics.tsv'
CAST_PATH = 'title.principals.tsv' # This holds the relationships between actors and movies according to imdb_ids
MOVIES_PATH = 'title.basics.tsv'
OUTPUT_JSON_PATH = 'movie_database.json'

MAX_ACTORS = 10000000
MAX_CAST = 20000000
MAX_MOVIES = 10000000

# TSV FIELD COUNTS
ACTOR_NUM_FIELDS = 6
CAST_NUM_FIELDS = 6
MOVIE_NUM_FIELDS = 9


def read_tsv_lines(file_path: str, max_rows: int) -> List[List[str]]:
    """
    Reads a TSV file, skips the header, and returns up to max_rows split lines.
    Each line is split into parts using tab.

    :param file_path: Path to the TSV file.
    :param max_rows: Maximum number of lines to read.
    :return: List of list of strings (split parts).
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        next(f)  # Skip header

        for i, line in enumerate(f):
            if i <= max_rows:
                yield line.strip().split('\t')

# LOADERS
def load_actors(file_path: str, max_rows) -> Dict[str, Actor]:
    """
    Loads actors from IMDb's name.basics.tsv file.

    :param file_path: Path to the name.basics.tsv file.
    :param max_rows: Max number of rows to read.
    :return: A dict mapping IMDb ID to Actor object.
    """
    imdb_to_actor = {}

    for i, parts in enumerate(read_tsv_lines(file_path, max_rows)):
        if len(parts) == ACTOR_NUM_FIELDS:
            imdb_id, name, _, _, professions_str, _ = parts
            professions = professions_str.split(',')

            if any(prof in professions for prof in ("actor", "actress")):
                actor = Actor(imdb_id, name)
                imdb_to_actor[imdb_id] = actor
        else:
            print(f"Line number {i} in actors table doesn't match the required number of fields {ACTOR_NUM_FIELDS}.")


    return imdb_to_actor


def load_cast(
    file_path: str,
    imdb_to_actor: Dict[str, Actor],
    max_rows: int
) -> Dict[str, List[int]]:
    """
    Loads movie-to-actor relationships from IMDb's title.principals.tsv file.

    :param file_path: Path to the title.principals.tsv file.
    :param imdb_to_actor: Lookup from IMDb actor ID to Actor object.
    :param max_rows: Max number of rows to read.
    :return: A dictionary mapping movie IMDb IDs to lists of internal actor IDs.
    """
    cast = {}

    for i, parts in enumerate(read_tsv_lines(file_path, max_rows)):
        if len(parts) == CAST_NUM_FIELDS:
            movie_id, _, actor_id, category, _, _ = parts
            actor = imdb_to_actor.get(actor_id)

            if category in {"actor", "actress"} and actor:
                cast.setdefault(movie_id, []).append(actor.id)
        else:
            print(f"Line number {i} in cast table doesn't match the required number of fields {CAST_NUM_FIELDS}.")


    return cast


def load_movies(
    file_path: str,
    cast: Dict[str, List[int]],
    max_rows
) -> List[Movie]:
    """
    Loads movies from IMDb's title.basics.tsv file and attaches cast.

    :param file_path: Path to the title.basics.tsv file.
    :param cast: Dictionary mapping movie IMDb ID to actor IDs.
    :param max_rows: Max number of rows to read.
    :return: List of Movie objects.
    """
    movies = []

    for i, parts in enumerate(read_tsv_lines(file_path, max_rows)):
        if len(parts) == MOVIE_NUM_FIELDS:
            imdb_id, title_type, title, _, _, _, _, _, _ = parts

            if title_type == "movie":
                movie = Movie(imdb_id, title)
                for actor_id in cast.get(imdb_id, []):
                    movie.add_actor(actor_id)
                movies.append(movie)
        else:
            print(f"Line number {i} in cast table doesn't match the required number of fields {MOVIE_NUM_FIELDS}.")


    return movies


# EXPORT TO FILE
def save_to_json(actors: List[Actor], movies: List[Movie], out_path: str) -> None:
    """
    Saves actors and movies to a JSON file.

    :param actors: List of Actor objects.
    :param movies: List of Movie objects.
    :param out_path: Path to the output JSON file.
    """
    data = {
        "actors": [actor.to_dict() for actor in actors],
        "movies": [movie.to_dict() for movie in movies],
    }

    try:
        with open(out_path, 'wb') as f:
            json_data = orjson.dumps(data, option=orjson.OPT_INDENT_2)
            f.write(json_data)
        print(f"Data saved to {out_path} (actors: {len(actors)}, movies: {len(movies)})")
    except IOError as e:
        print(f"Failed to write to {out_path}: {e}")


def main():
    download_all_imdb_datasets()

    print(f"{datetime.now().strftime('%H:%M:%S')} Loading actors...")
    imdb_to_actor = load_actors(ACTORS_PATH, max_rows=MAX_ACTORS)
    print(f"{datetime.now().strftime('%H:%M:%S')} Loaded {len(imdb_to_actor)} actors.")

    print(f"{datetime.now().strftime('%H:%M:%S')} Loading cast...")
    cast = load_cast(CAST_PATH, imdb_to_actor, max_rows=MAX_CAST)
    print(f"{datetime.now().strftime('%H:%M:%S')} Loaded cast for {len(cast)} movies.")

    print(f"{datetime.now().strftime('%H:%M:%S')} Loading movies...")
    movies = load_movies(MOVIES_PATH, cast, max_rows=MAX_MOVIES)
    print(f"{datetime.now().strftime('%H:%M:%S')} Loaded {len(movies)} movies.")

    print(f"{datetime.now().strftime('%H:%M:%S')} Saving to JSON...")
    save_to_json(imdb_to_actor.values(), movies, OUTPUT_JSON_PATH)

    print(f"{datetime.now().strftime('%H:%M:%S')} Done.")


if __name__ == "__main__":
    main()