import requests
from bs4 import BeautifulSoup
import re

headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Referer': 'https://www.marines.mil/News/Messages/MARADMINS/',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }

def extract_body_text(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        body_text = soup.find('div', class_='body-text')
        if body_text:
            return body_text.get_text(separator='\n', strip=True)
        else:
            return "Body text not found."
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {e}"

def get_maradmin_number(url):
    match = re.search(r'Messages-Display/Article/(\d+)/', url)
    return match.group(1) if match else "Unknown"

def get_maradmin_urls(base_url):
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    return [link['href'] for link in links if '/Messages-Display/Article/' in link['href']]

# Base URL for MARADMIN messages
urls = []
for i in range(2):
    base_url = "https://www.marines.mil/News/Messages/MARADMINS/?Page=" + str(i+1)
    urls = urls + get_maradmin_urls(base_url)

for url in urls:
    maradmin_number = get_maradmin_number(url)
    content = extract_body_text(url)
    with open(f"MARADMIN_{maradmin_number}.txt", "w") as file:
        file.write(content + "\n")
    print(f"Saved content from {url} to MARADMIN_{maradmin_number}.txt")