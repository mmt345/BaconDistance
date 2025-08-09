from typing import Dict, List, Set, Union


class Movie:
    """
    Represents a movie with a unique internal ID, IMDb ID, title, and a set of internal actor IDs.
    """
    # class var
    _counter = 1

    def __init__(self, imdb_id: str, title: str) -> None:
        """
        :param imdb_id: IMDb ID of the movie.
        :param title: Primary title of the movie.
        """
        self.id = Movie._counter
        Movie._counter += 1
        self.imdb_id = imdb_id
        self.title = title
        self.cast: Set[int] = set()

    def add_actor(self, internal_actor_id: int) -> None:
        """
        Adds an actor to the movie's cast.

        :param internal_actor_id: Internal ID of the actor.
        """
        self.cast.add(internal_actor_id)

    def to_dict(self) -> Dict[str, Union[str,int,List[int]]]:
        """
        :return: Dictionary representation of the movie.
        """
        return {
            "id": self.id,
            "imdb_id": self.imdb_id,
            "movie_title": self.title,
            "cast": list(self.cast)
        }
