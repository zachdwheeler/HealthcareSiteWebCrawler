from bs4 import BeautifulSoup
import requests

#sleep on this function and see if you can make it shorter tmr. There is a def a better to do this. 
def find_final_page_number(base_url):

    #Count variable keeps track of the current page number being checked
    count = 0
    
    #variable to indicate if the end page has been found
    found_end_page = False

    #variables to indiciated if we have found limits for each step size
    found_1000_limit = False
    found_100_limit = False
    found_10_limit = False
    try:
        while found_1000_limit == False:
            count += 1000
            current_url = base_url + str(count)

            #This gets the raw page data
            response = requests.get(current_url)

            try:

                #This checks to see if there were any errors when retrieving the page. Ex: a 404 page not found error
                response.raise_for_status()

                #This turns the page into html data that we can check to see if its valid
                soup = BeautifulSoup(response.content, 'html.parser')
                container = soup.find("div", class_="filter-result")
                
                #if there is nothing returned by the search, there is no page and hence we have gone too far and 
                #it therefore goes back a step
                if container is None:
                    count -= 1000
                    hit1000 = True
            except requests.exceptions.HTTPError as e:
                print(f"Request failed: {e}")
            
            
        while found_100_limit == False:
            count += 100

            current_url = base_url + str(count)
            response = requests.get(current_url)

            try:
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                container = soup.find("div", class_="filter-result")

                if container is None:
                    count -= 100
                    hit100 = True
            except requests.exceptions.HTTPError as e:
                print(f"Request failed: {e}")
            
        while found_10_limit == False:
            count += 10

            current_url = base_url + str(count)
            response = requests.get(current_url)

            try:
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                container = soup.find("div", class_="filter-result")
                
                if container is None:
                    count -= 10
                    hit10 = True
            except requests.exceptions.HTTPError as e:
                print(f"Request failed: {e}")
        
        while found_end_page == False:
            count += 1

            current_url = base_url + str(count)
            response = requests.get(current_url)

            try:
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                container = soup.find("div", class_="filter-result")
                
                if container is None:
                    return count-1
            except requests.exceptions.HTTPError as e:
                print(f"Request failed: {e}")
    except:
        print(f"An error occured when trying to access page {count}")