from typing import Dict, Union


class Actor:
    """
    Represents an actor with a unique internal ID, IMDb ID, and name.
    """
    # class var
    _counter = 1

    def __init__(self, imdb_id: str, name: str) -> None:
        """
        :param imdb_id: IMDb ID of the actor.
        :param name: Full name of the actor.
        """
        self.id = Actor._counter
        Actor._counter += 1
        self.imdb_id = imdb_id
        self.name = name

    def to_dict(self) -> Dict[str, Union[str,int]]:
        """
        :return: Dictionary representation of the actor.
        """
        return {
            "id": self.id,
            "imdb_id": self.imdb_id,
            "name": self.name
        }
