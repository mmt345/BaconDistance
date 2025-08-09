import os
import gzip
from shutil import copyfileobj
from urllib.request import urlretrieve

FILES = {
    "name.basics.tsv": "https://datasets.imdbws.com/name.basics.tsv.gz",
    "title.basics.tsv": "https://datasets.imdbws.com/title.basics.tsv.gz",
    "title.principals.tsv": "https://datasets.imdbws.com/title.principals.tsv.gz"
}

def download_and_extract(target_file_name: str, url: str) -> None:
    """
    Downloads the TSV file from the website and extracts the content of the file
    if the file already exits it won't be downloaded, and if only the gz exits it will get extracted.

    :param target_file_name: the name of the TSV file.
    :param url: the url from which to download the file.
    """
    gz_file_name = target_file_name + ".gz"

    if os.path.exists(target_file_name):
        print(f"{target_file_name} won't be downloaded, already exists!")
        return

    # Download .gz if not already downloaded
    if not os.path.exists(gz_file_name):
        print(f"Downloading {gz_file_name}")
        urlretrieve(url, gz_file_name)
        print(f"Downloaded {gz_file_name}")
    else:
        print(f"{gz_file_name} won't be downloaded, already exists!")

    # Extract .gz file
    print(f"Extracting {gz_file_name}")
    with gzip.open(gz_file_name, 'rb') as gz_file:
        with open(target_file_name, 'wb') as target_file:
            copyfileobj(gz_file, target_file)
    print(f"Extracted to {target_file_name}")

def download_all_imdb_datasets() -> None:
    """
    Downloads the TSV files from the imdb website and extracts their content.
    """
    for filename, url in FILES.items():
        download_and_extract(filename, url)


if __name__ == "__main__":
    download_all_imdb_datasets()