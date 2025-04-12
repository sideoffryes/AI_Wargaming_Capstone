import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

error_count = 0

headers = {
    "Host": "www.marines.mil",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Cookie": "mdm-view506=list",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

session = requests.Session()
session.headers.update(headers)

def extract_body_text(url):
    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        body_text = soup.find('div', class_='body-text')
        if body_text:
            return body_text.get_text(separator='\n', strip=True)
        else:
            return "Body text not found."
    except requests.exceptions.RequestException as e:
        global error_count
        error_count += 1
        return ""

def get_maradmin_number(url):
    match = re.search(r'Messages-Display/Article/(\d+)/', url)
    return match.group(1) if match else "Unknown"

def get_maradmin_urls(base_url):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        return [link['href'] for link in links if '/Messages-Display/Article/' in link['href']]
    except Exception as e:
        global error_count
        error_count += 1
        return ""

# Base URL for MARADMIN messages
urls = []
# Change value inside of range to modify how many pages of MARADMINS to download
for i in range(50):
    base_url = "https://www.marines.mil/News/Messages/MARADMINS/?Page=" + str(i+1)
    urls = urls + get_maradmin_urls(base_url)

for url in tqdm(urls, desc="Downloading MARADMINS"):
    maradmin_number = get_maradmin_number(url)
    content = extract_body_text(url)
    if content:
        with open(f"./data/MARADMINS/MARADMIN_{maradmin_number}.txt", "w") as file:
            file.write(content + "\n")
            
print(f"Total number of errors during MARADMIN requests: {error_count}")