import requests
from bs4 import BeautifulSoup

page_url = "https://archive.org/details/kappa-magazine"

response = requests.get(page_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

    print("Links to pdf:")
    for link in pdf_links:
        print(f"https://archive.org{link}")
else:
    print(f"Error loading page: {response.status_code}")
