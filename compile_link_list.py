#py -m pip install -r requirements.txt (run in powershell)

from bs4 import BeautifulSoup
import requests


def find_final_page_number(base_url):
    count = 0
    step = 1000
    while True:
        count += step
        if not check_page_exists(base_url + str(count)):
            count -= step
            step = step//2
        else:
            if step == 1:
                break
    return count


def check_page_exists(url):
    response = requests.get(url)
    try:
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        container = soup.find("div", class_="filter-result")
                
        if container is None:
            return False
        else:
            return True
    except requests.exceptions.HTTPError as e:
        print(f"Request failed: {e}")

print(find_final_page_number("https://www.zorgkaartnederland.nl/?zoekterm=%20&p="))