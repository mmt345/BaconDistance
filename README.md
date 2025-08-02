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