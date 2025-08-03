import argparse
import math
from actor_graph import ActorGraph
from typing import Optional


def calculate_and_print_distance(graph: ActorGraph, from_actor: str, to_actor: Optional[str] = "Kevin Bacon") -> None:
    """
    Calculates and prints the Bacon distance between two actors.
    Handles cases where actors do not exist in the graph.

    :param graph: The ActorGraph object.
    :param from_actor: Starting actor name.
    :param to_actor: Target actor name (default is Kevin Bacon).
    """
    if from_actor not in graph.graph:
        print(f"Error: Actor '{from_actor}' not found in database.")
        return

    if to_actor not in graph.graph:
        print(f"Error: Actor '{to_actor}' not found in database.")
        return

    distance = graph.bacon_distance(from_actor, to_actor)

    if distance == math.inf:
        print(f"No connection found between '{from_actor}' and '{to_actor}'.")
    else:
        print(f"Bacon distance between '{from_actor}' and '{to_actor}': {distance}")


def main():
    """
    Entry point for calculating the Bacon distance between actors.
    If --from_actor is not provided, enters interactive mode to query multiple distances.
    """
    parser = argparse.ArgumentParser(
        description="Calculate the Bacon distance between actors "
                    "based on co-appearances in movies."
    )

    parser.add_argument(
        "--from_actor",
        type=str,
        help="Name of the starting actor (use for single calculation)"
    )

    parser.add_argument(
        "--to_actor",
        type=str,
        default="Kevin Bacon",
        help="Name of the target actor (default: Kevin Bacon)"
    )

    parser.add_argument(
        "--json_file",
        type=str,
        default="movie_database.json",
        help="Path to the JSON file containing actor and movie data (default: movie_database.json)"
    )

    args = parser.parse_args()
    graph = ActorGraph.load_from_json(args.json_file)

    if args.from_actor:
        # Single calculation mode
        calculate_and_print_distance(graph, args.from_actor, args.to_actor)
    else:
        # Interactive mode
        print("Interactive Bacon Distance Calculator. Enter actor names (Ctrl+C to exit).")
        print("Format: <actor> or <actor1>,<actor2>\n")

        try:
            while True:
                line = input("Enter actor(s): ").strip()
                if line:
                    actors = [name.strip() for name in line.split(',')]
                    if len(actors) == 1:
                        calculate_and_print_distance(graph, actors[0])
                    elif len(actors) == 2:
                        calculate_and_print_distance(graph, actors[0], actors[1])
                    else:
                        print("Invalid input format. Use: <actor> or <actor1>,<actor2>")
                else:
                    print("No input was given.if you want to exit -> Press Ctrl+C")
        except KeyboardInterrupt:
            print("\nExiting.")


if __name__ == "__main__":
    main()
