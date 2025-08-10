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

# Bacon Distance – Milestone 2

This milestone adds a basic website for calculating the Bacon distance between two actors.

## Included Functionality

- A homepage (`/`) with a form to enter actor names.
- A result page that shows the Bacon distance or an error.
- Uses Flask for the server and Bootstrap for styling.
- Loads the actor graph from `movie_database.json` (one time in the beginning).

## Run Instructions

1. Make sure `movie_database.json` exists (from Milestone 0).
2. Install Flask:
   ```bash
   pip install flask
   ```
3. Run the server:
   ```bash
   python bacon_server.py
   ```
4. Open your browser at:
   ```
   http://localhost:5000/
   ```

# Bacon Distance – Milestone 3

## Overview
In this milestone, I containerized my bacon website using **Docker** and **Docker Compose**.  
The goal is to make the application runnable on any machine with only Docker and Git installed.

The IMDb database (`movie_database.json`) is generated once during the Docker image build.  
Docker layer caching ensures that the database is not regenerated unless generate_db (or other db related files in db folder) changes.

## Run Instructions
1. Clone the repository and switch to the milestone tag:
    ```bash
    git clone <my_github_repo>
    cd project_name (BaconDistance)
    git checkout milestone-3
    ```
2. Build and start the container:
    ```bash
    docker compose up -d
    ```
3. Open the site in your browser:
    ```
    http://localhost
    ```

# Bacon Distance – Milestone 4

## Overview
In this milestone, the project was upgraded to use **PostgreSQL** with **Docker Compose profiles** for flexible startup options:  
- **`generate_db`** – Builds the database from IMDb source files before starting the web server (first-time setup or refresh).  (about 20 minutes to generate the entire db)
- **`no_generate_db`** – Starts the app using the existing database without rebuilding it (faster startup).  

PostgreSQL runs in its own container with a persistent volume so data survives restarts, there are also health checks that ensure the web server starts only after the database is ready (and after data generation, if requested)
---
## Why PostgreSQL (SQL vs NoSQL)
- **Relational fit** – Actors and movies form a relationship, mapping naturally to relational tables and foreign keys.
- **ORM-friendly** – Works great with SQLAlchemy. 
**Not NoSQL:** Document stores like MongoDB are less efficient for relationship queries.  
---

## Run Instructions

1. Clone & switch to milestone:
   ```bash
   git clone <my_github_repo>
   cd project_name (BaconDistance)
   git checkout milestone-4
   ```
2. Run with DB generation:
   ```bash
   docker compose --profile generate_db up -d
   ```
2. Run without DB generation:
   ```bash
   docker compose --profile no_generate_db up -d
   ```
3. Open in browser:
   ```
   http://localhost
   ```
**Reset database:**
```bash
docker compose down -v
```