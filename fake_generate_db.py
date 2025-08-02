import json
from typing import List, Dict

class Actor:
    actors_counter: int = 1  # Class-level counter for actors

    def __init__(self, name: str) -> None:
        """
        Initializes an actor object with a name and a unique ID.

        :param name: The name of the actor.
        :return: None
        """
        self.name = name
        self.actor_id = Actor.actors_counter
        Actor.actors_counter += 1  # Increment the actor ID for the next actor

    def to_dict(self) -> Dict[str, int]:
        """
        Converts the actor object to a dictionary format.

        :return: dict: A dictionary representing the actor with 'id' and 'name' keys.
        """
        return {
            'id': self.actor_id,
            'name': self.name
        }


class Movie:
    movies_counter: int = 1  # Class-level counter for movies

    def __init__(self, movie_title: str) -> None:
        """
        Initializes a movie object with a title, unique ID, and a set of actors.

        :param movie_title: The title of the movie.
        :return: None
        """
        self.movie_id = Movie.movies_counter
        Movie.movies_counter += 1 
        self.movie_title = movie_title
        self.cast: set[int] = set()  # A set of actor IDs that participated in the movie

    def add_actor(self, actor_id: int) -> None:
        """
        Adds an actor to the movie's cast by their ID.

        :param actor_id: The unique ID of the actor to be added to the cast.
        :return: None
        """
        self.cast.add(actor_id)

    def to_dict(self) -> Dict[str, List[int]]:
        """
        Converts the movie object to a dictionary format.

        :return: dict: A dictionary representing the movie with 'id', 'movie_title', and 'cast' keys.
        """
        return {
            'id': self.movie_id,
            'movie_title': self.movie_title,
            'cast': list(self.cast)  # List of actor IDs in the cast
        }

# Function to save the actors and movies data to a JSON file.
def save_to_json(actors: List[Actor], movies: List[Movie], filename: str) -> None:
    """
    Saves the list of actors and movies to a JSON file.

    :param actors: A list of Actor objects.
    :param movies: A list of Movie objects.
    :param filename: The name of the file to save the data to.
    
    :return: None: This function saves the data to the specified file.
    """
    actors_dict = [actor.to_dict() for actor in actors]
    movies_dict = [movie.to_dict() for movie in movies]

    data = {
        'movies': movies_dict,
        'actors': actors_dict
    }

    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print(f"Data saved to {filename}")

# Function to load the actors and movies data from a JSON file.
def load_from_json(filename: str) -> tuple[Dict[int, Actor], Dict[int, Movie]]:
    """
    Loads actors and movies data from a JSON file and returns them as objects.

    :param filename: The name of the JSON file to load data from.
    
    :return: tuple: A tuple containing a dictionary of actors (key: actor_id, value: Actor object)
                     and a dictionary of movies (key: movie_id, value: Movie object).
    """
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    
    actors: Dict[int, Actor] = {}
    movies: Dict[int, Movie] = {}

    # Creating actor objects from loaded data
    for actor_data in data['actors']:
        actor = Actor(actor_data['name'])
        actors[actor_data['id']] = actor

    # Creating movie objects from loaded data
    for movie_data in data['movies']:
        movie = Movie(movie_data['movie_title'])
        movies[movie_data['id']] = movie

    # Linking actors to movies they participated in
    for movie_data in data['movies']:
        movie = movies[movie_data['id']]
        for actor_id in movie_data['cast']:
            actor = actors[actor_id]
            movie.add_actor(actor.actor_id)

    return actors, movies

# Main function to create sample actors and movies, and save the data to a JSON file.
def main() -> None:
    """
    Initializes sample actors and movies, links actors to movies, and saves the data to a JSON file.

    :return: None: This function does not return anything.
    """
    # Create actors and movies
    actors = [Actor("Kevin Bacon"), Actor("Tom Hanks"), Actor("Paul Walker"), Actor("Gal Gadot"), 
    Actor("Ben Affleck"), Actor("Henry Cavill"), Actor("Vin Diesel"), Actor("Chris Pratt")]

    movie1 = Movie("Apollo 13")
    movie2 = Movie("Fast and Furious 4")
    movie3 = Movie("Justice League")
    movie4 = Movie("The Guardians of the Galaxy Holiday Special")

    movie1.add_actor(1)
    movie1.add_actor(2)
    movie2.add_actor(3)
    movie2.add_actor(4)
    movie2.add_actor(7)

    movie3.add_actor(4)
    movie3.add_actor(5)
    movie3.add_actor(6)

    movie4.add_actor(7)
    movie4.add_actor(1)
    movie4.add_actor(8)

    movies = [movie1, movie2, movie3, movie4]

    # Save data to JSON
    save_to_json(actors, movies, 'movie_database.json')

if __name__ == '__main__':
    main()
