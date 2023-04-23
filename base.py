import requests
import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup

proxies = { # use Clash proxy, default port 7890
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}
headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
}

def get_PageContent_from_URL(url):
    global proxies, headers  
    response = requests.get(url, verify=False, proxies = proxies, headers=headers)
    html_content = response.content
    page_content = BeautifulSoup(html_content, "html.parser")
    return page_content

# return a list of elemtnets satisfying the attribute constrain 
def get_element_with_attribute(soup, attribute_name, attribute_value): 
    # Find all elements that have this attribute
    candidates = soup.select("[" + attribute_name + "]")
    goal_list = []

    for element in candidates:
        if element.get(attribute_name) == attribute_value:
            goal_list.append(element)

    return goal_list

if __name__ == "__main__":
    url_top250 = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    soup = get_PageContent_from_URL(url_top250)
    table = get_element_with_attribute(soup, "data-caller-name", "chart-top250movie")[0]
    print(table)
