from flask import Flask, request, render_template
from actor_graph import ActorGraph
import math

app = Flask(__name__)

# Load the graph once when the server starts
ACTORS_GRAPH = ActorGraph.load_from_json("movie_database.json")

@app.route("/")
def home():
    """
    Renders the home page with the Bacon Distance input form.

    :return: Rendered HTML template of the home page.
    """
    return render_template("home.html")


@app.route("/bacon_distance", methods=["GET"])
def bacon_distance():
    """
    Endpoint to calculate the Bacon distance between two actors.

    This endpoint receives actor names via query parameters and returns the 
    Bacon distance between them, based on a preloaded actor graph.

    :param from_actor: The name of the starting actor. (Required, str)

    :param to_actor: The name of the target actor. Defaults to "Kevin Bacon" if not provided. (str)

    :return: Rendered HTML template with the result or error message.
    """
    from_actor = (request.args.get("from_actor") or "").strip().title()
    to_actor = (request.args.get("to_actor") or "Kevin Bacon").strip().title()

    if not from_actor:
        return render_template("result.html", error="Missing 'from_actor' parameter.")

    if from_actor not in ACTORS_GRAPH.graph:
        return render_template("result.html", error=f"Actor '{from_actor}' not found.")

    if to_actor not in ACTORS_GRAPH.graph:
        return render_template("result.html", error=f"Actor '{to_actor}' not found.")

    distance = ACTORS_GRAPH.bacon_distance(from_actor, to_actor)

    if distance == math.inf:
        return render_template(
            "result.html",
            from_actor=from_actor,
            to_actor=to_actor,
            distance=None
        )

    return render_template(
        "result.html",
        from_actor=from_actor,
        to_actor=to_actor,
        distance=distance
    )

if __name__ == "__main__":
    app.run(debug=True)
