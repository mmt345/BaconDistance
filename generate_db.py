import json
OUTPUT_FILENAME = "basic_db.json"
MOVIES_DATA = [
    {
        "name": "Fast and Furious 4",
        "actors": ["Vin Diesel", "Gal Gadot", "Paul Walker"]
    },
    {
        "name": "Justice League",
        "actors": ["Ben Affleck", "Gal Gadot", "Henry Cavill"]
    },
    {
        "name": "Apollo 13",
        "actors": ["Tom Hanks", "Kevin Bacon", "Bill Paxton"]
    },
    {
        "name": "The Guardians of the Galaxy Holiday Special",
        "actors": ["Vin Diesel", "Kevin Bacon", "Chris Pratt"]
    },
    {
        "name": "Inception",
        "actors": ["Leonardo DiCaprio", "Tom Hardy", "Joseph Gordon-Levitt"]
    }
]

def generate_database(filename:str=OUTPUT_FILENAME) -> None:
    output = {"movies": MOVIES_DATA}
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Your information was written to {filename}")

if __name__ == "__main__":
    generate_database()

