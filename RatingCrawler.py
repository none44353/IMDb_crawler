from base import get_PageContent_from_URL, get_element_with_attribute
from urllib.parse import urljoin
import time

base_URL = "https://www.imdb.com/"
waiting_time = 0.25 # The waiting time duration(s) when the target page is not fetched.

def get_value(text):
    string_value = list(filter((lambda x: len(x) > 0), text.split("\n")))[0]
    string_value = string_value.replace(",", "")
    return int(string_value)


# get rating from a 
def get_rating_from_Ratingpage(Ratingpage_URL):    
    getRightPage, Ratingpage, subpage = False, None, None
    # The IMDB server does not always return my desire page. Keep trying until you get what you want.
    while(not getRightPage):
        try:
            Ratingpage = get_PageContent_from_URL(Ratingpage_URL)
            subpage = get_element_with_attribute(Ratingpage, "class", ["title-ratings-sub-page"])[0]
            getRightPage = True
        except:
            print("[Error]: The target page was not fetched. Fail to get the subpage element. Try again later ...")
            # file = open("wrong_rating_page.html", "w", encoding="utf-8")
            # file.write(str(Ratingpage))
            time.sleep(waiting_time)
            
    textcontent = subpage.find('div', {'class': 'allText'}).find('div', {'class': 'allText'})
    votingTable = textcontent.find('table', {'cellpadding': "0"})
    rows = votingTable.find_all('tr')
    
    votes = {}
    for row in rows[1:]:
        columns = row.find_all('td')
        votes[get_value(columns[0].text)] = get_value(columns[-1].text)

    meanDiv = textcontent.find('div', {'class': 'allText', 'align':'center'})
    meanText = list(x.lstrip() for x in filter((lambda x: len(x) > 0), meanDiv.text.split("\n")))
    ArMean = float(meanText[0].split(' ')[-1])
    Median = float(meanText[2].split(' ')[-1])
    return votes, ArMean, Median

Location = {
    "All": (1, 1, 1), #All group对应的是第二张表中(表的标号从0开始)，内容的第一行、第一列（第二张表的行列都有表头）
    "<18": (1, 1, 2), 
    "18-29": (1, 1, 3), 
    "30-44": (1, 1, 4), 
    "45+": (1, 1, 5), 
    "Males": (1, 2, 1), 
    "Females": (1, 3, 1), 
    "Top 1000 Voters": (2, 1, 0), 
    "US Users": (2, 1, 1), 
    "Non-US Users": (2, 1, 2), 
}

def get_rating_by_groups_from_movieHomepage(Homepage_URL):
    movieHomepage = get_PageContent_from_URL(Homepage_URL)
    # homefile = open("home_page.html", "w", encoding="utf-8")
    # homefile.write(str(movieHomepage))

    RatingButton = get_element_with_attribute(movieHomepage, "data-testid", "hero-rating-bar__aggregate-rating")[0]
    Ratingpage_href = RatingButton.select("[href]")[0].get("href")
    Ratingpage_URL = urljoin(base_URL, Ratingpage_href)
    getRightPage, Ratingpage, subpage = False, None, None
    # The IMDB server does not always return my desire page. Keep trying until you get what you want.
    while(not getRightPage):
        try:
            Ratingpage = get_PageContent_from_URL(Ratingpage_URL)
            subpage = get_element_with_attribute(Ratingpage, "class", ["title-ratings-sub-page"])[0]
            getRightPage = True
        except:
            print("[Error]: The target page was not fetched. Fail to get the subpage element. Try again later ...")
            # file = open("wrong_rating_page.html", "w", encoding="utf-8")
            # file.write(str(Ratingpage))
            time.sleep(waiting_time)

    textcontent = subpage.find('div', {'class': 'allText'}).find('div', {'class': 'allText'})
    tables = textcontent.find_all('table')

    rating = {}
    for group_name, pos in Location.items():
        table = tables[pos[0]]
        rows = table.find_all('tr')
        row = rows[pos[1]]
        columns = row.find_all('td')
        cell = columns[pos[2]]

        value = {}
        value["#Voters"] = get_value(cell.find('div', {'class': 'smallcell'}).text)
        value["Weighted Average Ratings"] = float(cell.find('div', {'class': 'bigcell'}).text)
        
        href = cell.select("[href]")[0].get("href")
        url = urljoin(base_URL, href)
        distribution, AMean, Median = get_rating_from_Ratingpage(url)
        value["Arithmetic mean"] = AMean
        value["Median"] = Median
        value["Distribution"] = distribution
        
        rating[group_name] = value
    return rating


if __name__ == "__main__":
    test_url = "https://www.imdb.com/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=1a264172-ae11-42e4-8ef7-7fed1973bb8f&pf_rd_r=XGBTH3XS7AVC3NASTNGS&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_1"
    print(get_rating_by_groups_from_movieHomepage(test_url))