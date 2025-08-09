# BaconDistance

# Bacon Distance – Milestone 0

This Milestone prepares the initial dataset for the Bacon Distance project.

## Overview
I process IMDb TSV files to create a JSON file containing:

- A list of actors with internal IDs, names, and IMDb IDs.
- A list of movies with internal IDs, titles, IMDb IDs, and cast (as actor IDs).

## Run Instructions

1. Download and unzip IMDb datasets from:  
   https://developer.imdb.com/non-commercial-datasets/

2. Place the following files in the root folder (as we ignore them in this git project):
   - `name.basics.tsv`
   - `title.basics.tsv`
   - `title.principals.tsv`

3. Run the script:
    python generate_db.py
    Output: movie_database.json

# Bacon Distance – Milestone 1

This milestone builds the logic for calculating Bacon distances using the movie-actor dataset we previously made

## Overview

We implement a graph of actors where:

- Each actor is a node.
- An edge connects two actors if they appeared in the same movie.
- We support calculating the shortest connection (Bacon distance) between any two actors using **Breadth-First Search (BFS)**.

The graph is built once from the JSON file and reused for all queries.

## Included Functionality

- `ActorGraph` class with:
  - Efficient BFS implementation (`bacon_distance`)
  - Graph construction from `movie_database.json`

- `bacon_distance.py`:
  - Command-line tool to compute Bacon distance between any two actors
  - Optional interactive mode for querying multiple distances

## Run Instructions

1. Make sure you have `movie_database.json` (generated from Milestone 0).
   If not, follow the instructions in `Milestone 0`.

2. Run one of the following:

### Single Distance Calculation:

```bash
python bacon_distance.py --from_actor "Tom Hanks"
```

### Two actors Distance Calculation:
```bash
python bacon_distance.py --from_actor "Vin Diesel" --to_actor "Gal Gadot"
```

### Interactive Mode:
```bash
python bacon_distance.py
```
