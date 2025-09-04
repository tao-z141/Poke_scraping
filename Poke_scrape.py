import os
import re
import time
import requests
from bs4 import BeautifulSoup
import boto3

S3_BUCKET = "pokescrape"
S3_PREFIX = "images"
DOWNLOAD_DELAY = 1
MAX_RETRIES = 3

s3 = boto3.client('s3')
URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_>HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_generation(pokedex_number):
    if 1 <= pokedex_number <= 151: return "Generation_I"
    elif 152 <= pokedex_number <= 251: return "Generation_II"
    elif 252 <= pokedex_number <= 386: return "Generation_III"
    elif 387 <= pokedex_number <= 493: return "Generation_IV"
    elif 494 <= pokedex_number <= 649: return "Generation_V"
    elif 650 <= pokedex_number <= 721: return "Generation_VI"
    elif 722 <= pokedex_number <= 809: return "Generation_VII"
    elif 810 <= pokedex_number <= 1010: return "Generation_VIII"
    else: return "Unknown"

def download_image(url, path):
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            with open(path, "wb") as f:
                f.write(r.content)
            return True
        except Exception as e:
            print(f"Erreur téléchargement {url}: {e} (tentative {attempt+1}/{MAX_RETRIES})")
            time.sleep(2)
    return False

def main():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all("table", class_="roundy")
    print(f"Found {len(tables)} generation tables")

    for table in tables:
        for row in table.find_all("tr")[1:]:  
            cols = row.find_all("td")
            if len(cols) < 2:
                continue

            # Numéro du Pokédex
            num_text = cols[0].text.strip().lstrip("#")
            if not num_text.isdigit():
                continue
            pokedex_number = int(num_text)
            generation = get_generation(pokedex_number)

            # URL de l'image
            img_tag = cols[1].find("img")
            if not img_tag:
                continue
            img_url = img_tag.get("src")
            img_name = os.path.basename(img_url)

            local_folder = f"./{generation}"
            os.makedirs(local_folder, exist_ok=True)
            local_path = f"{local_folder}/{img_name}"

            if os.path.exists(local_path):
                print(f"Skip {img_name}, déjà téléchargée.")
                continue

            if download_image(img_url, local_path):
                print(f"Downloaded {img_name} into {generation}")
            else:
                print(f"Failed to download {img_name}, skipping.")
                continue

            # Upload sur S3
            try:
                s3.upload_file(local_path, S3_BUCKET, f"{S3_PREFIX}/{generation}/{img_name}")
                print(f"Uploaded {img_name} to S3/{S3_PREFIX}/{generation}/")
            except Exception as e:
                print(f"Erreur upload {img_name} sur S3: {e}")

            time.sleep(DOWNLOAD_DELAY)

if __name__ == "__main__":
    main()
