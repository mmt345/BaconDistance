import orjson
import math
from typing import Dict, Set, Tuple
from collections import deque
from itertools import combinations


class ActorGraph:
    """
    A graph representing connections between actors who have acted together in movies.
    """

    def __init__(self) -> None:
        self.graph: Dict[str, Set[str]] = {}

    def add_coappearance(self, actor_name_a: str, actor_name_b: str) -> None:
        """
        Adds a bi-directional edge between two actors, indicating they co-starred in a movie.

        :param actor_name_a: Name of the first actor.
        :param actor_name_b: Name of the second actor.
        """
        if actor_name_a == actor_name_b:
            return  # Skip self-links
        self.graph.setdefault(actor_name_a, set()).add(actor_name_b)
        self.graph.setdefault(actor_name_b, set()).add(actor_name_a)

    def get_coactors(self, actor_name: str) -> Set[str]:
        """
        Retrieves all actors who have co-starred with the given actor.

        :param actor_name: The name of the actor.
        :return: A set of co-actor names.
        """
        return self.graph.get(actor_name, set())

    def bacon_distance(self, from_actor: str, to_actor: str = "Kevin Bacon") -> int:
        """
        Calculates the Bacon distance (shortest path) between two actors assuming both actors exist in the graph.
        using a Breadth-First Search (BFS) traversal on the co-actor graph.

        The Bacon distance is the minimum number of steps (shared movies) required to connect
        the starting actor to the target actor. If no connection exists, the function returns math.inf.
        If both actors are the same actor -> the distance is 0.

        :param from_actor: The name of the starting actor.
        :param to_actor: The name of the target actor. Defaults to "Kevin Bacon".
        :return: An integer representing the distance between the two actors,
                or math.inf if no connection exists.
        """
        if from_actor == to_actor:
            return 0

        visited: Set[str] = set()
        queue: deque[Tuple[str, int]] = deque([(from_actor, 0)])
        visited.add(from_actor)

        while queue:
            current_actor, distance = queue.popleft()

            if current_actor == to_actor:
                return distance

            for neighbor in self.get_coactors(current_actor):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))

        return math.inf

    @classmethod
    def load_from_json(cls, filename: str) -> "ActorGraph":
        """
        Loads actor and movie data from a JSON file and constructs a graph object
        where each actor is a node, and an edge exists between any two actors
        who appeared in the same movie.

        This implementation also ensures that actors who didn't appear in any movie
        are still represented as isolated nodes in the graph.

        :param filename: Path to the JSON file.
        :return: An ActorGraph instance representing the connections between actors.
        """
        with open(filename, 'rb') as f:
            data = orjson.loads(f.read())

        # Build mapping from internal actor ID to actor name
        id_to_name: Dict[int, str] = {
            actor["id"]: actor["name"]
            for actor in data["actors"]
        }

        graph = cls()

        # Ensure all actors are added to the graph, even if they are isolated
        for actor_name in id_to_name.values():
            graph.graph.setdefault(actor_name, set())

        for movie in data["movies"]:
            cast_ids = movie.get("cast", [])

            # Filter out unknown actor IDs (optional for safety)
            cast_names = [
                id_to_name[actor_id]
                for actor_id in cast_ids
                if actor_id in id_to_name
            ]

            # Create bidirectional edges between all actors in the same movie
            for actor1, actor2 in combinations(cast_names, 2):
                graph.add_coappearance(actor1, actor2)

        return graph
