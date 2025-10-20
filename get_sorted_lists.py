#py -m pip install -r requirements.txt (run in powershell)


from bs4 import BeautifulSoup
import requests
import re
import multiprocessing
from multiprocessing import Process
from multiprocessing import Pool

base_url = "https://www.zorgkaartnederland.nl/?zoekterm=%20&p="

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

def compile_search_link_list():
  max_page_num = find_final_page_number(base_url)
  search_page_links = []
  for i in range(max_page_num):
    search_page_links.append(base_url+str(i+1))
  return search_page_links

def compile_search_result_list(url):
    container_class = "filter-results" 
    target_classes = "filter-result__body"
    matching_container_class = "div"
    try:
      response = requests.get(url)
      response.raise_for_status()
      soup = BeautifulSoup(response.content, 'html.parser')

      container = soup.find(matching_container_class, class_=container_class)
      elements = container.find_all("div", class_=target_classes)
      if container is None:
        print(f"Could not find container with tag '{matching_container_class}' and class '{container_class}' on {url}")
      if elements is None:
        print(f"Could not find container with tag 'div' and class '{target_classes}' on {url}")
      # Find all elements with the specified column class
      link_list = []
      for element in elements:
        for link in element.find_all('a', class_="filter-result__name", href=True):
          link_list.append(link['href'])
      return link_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Link: {url}")

def get_complete_link_list():
  search_link_list = compile_search_link_list()
  temp_list = []
  complete_list = []
  with Pool(100) as p:
    temp_list = p.map(compile_search_result_list, search_link_list)
    complete_list = sum(temp_list, complete_list)
  return complete_list

def get():
  complete_list = get_complete_link_list()
  sorted_list = []
  institution_list = []
  professional_list = []

  for link in complete_list:
    if re.search('zorgverlener', link):
      institution_list.append(link)
    else:
      professional_list.append(link)
  
  return institution_list, professional_list