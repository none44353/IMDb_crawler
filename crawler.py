import requests
import urllib3
urllib3.disable_warnings()
from urllib.parse import urljoin
from bs4 import BeautifulSoup

base_url = "https://www.imdb.com/"
url_top250 = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}
headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
}

def get_element_with_attribute(soup, attribute_name, attribute_value): # return the first element with request attribute value
    # Find all elements that have this attribute
    candidates = soup.select("[" + attribute_name + "]")
    goal_element = None

    for element in candidates:
        if element.get(attribute_name) == attribute_value:
            goal_element = element
            break

    return goal_element

def table_parsing(table):
    global base_url
    movie_title, movie_link, IMDb_rating = [], [], []
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")
    print(len(rows))
    id = 0
    for row in rows:
        id = id + 1
        columns = row.find_all("td")
        for cell in columns:
            if (cell.get("class") == ["titleColumn"]):
                content = list(filter((lambda x: len(x) > 0), cell.text.split("\n")))
                content = [text.lstrip() for text in content]
                # content looks as ['1.', 'The Shawshank Redemption', '(1994)']
                movie_title.append(content[1])
                # produced_year.append(int(content[2][1:-1]))
                ref = cell.find("a")
                url_link = urljoin(base_url, ref.get("href"))
                movie_link.append(url_link)
            if (cell.get("class") == ["ratingColumn", "imdbRating"]):
                content = list(filter((lambda x: len(x) > 0), cell.text.split("\n")))
                content = [text.lstrip() for text in content]
                IMDb_rating.append(float(content[0]))
    return movie_title, movie_link, IMDb_rating

def get_PageContent_from_URL(url):
    global proxies, headers  
    response = requests.get(url, verify=False, proxies = proxies, headers=headers)
    html_content = response.content
    page_content = BeautifulSoup(html_content, "html.parser")
    return page_content


def get_rating_via_link(url):
    # to be done
    return

url_google = "https://www.google.com/"
# response = requests.get(url_top250, verify=False, proxies = proxies, headers=headers)
# html_content = response.content
# soup = BeautifulSoup(html_content, "html.parser")
soup = get_PageContent_from_URL(url_top250)
table = get_element_with_attribute(soup, "data-caller-name", "chart-top250movie")
assert(table.name == "table")
movie_title, movie_link, IMDb_rating = table_parsing(table)

for (title, link) in zip(movie_title, movie_link):
    get_rating_via_link(link)
    break

