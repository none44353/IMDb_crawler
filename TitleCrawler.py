from base import get_PageContent_from_URL, get_element_with_attribute
from urllib.parse import urljoin

base_url = "https://www.imdb.com/"

listInfo = {
    "Top250": ("https://www.imdb.com/chart/top/?ref_=nv_mv_250", "chart-top250movie"), 
    "Lowest100": ("https://www.imdb.com/chart/bottom?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=470df400-70d9-4f35-bb05-8646a1195842&pf_rd_r=1J9N00P07Q3Z81MS366T&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_ql_8", "chart-bttm100movie"), 
    "Popular100": ("https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm", "chart-moviemeter") 
}

def listParsing(table, isPopular100List):
    global base_url
    movie_title, movie_link, IMDb_rating = [], [], []
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")
    
    for row in rows:
        columns = row.find_all("td")
        for cell in columns:
            if (cell.get("class") == ["titleColumn"]):
                content = list(filter((lambda x: len(x) > 0), cell.text.split("\n")))
                content = [text.lstrip() for text in content]
                # content looks as ['1.', 'The Shawshank Redemption', '(1994)'] for Top250 and Lowest100
                #                  ['The Super Mario Bros. Movie', '(2023)', '1', '(no change)'] for Popular100
                
                title, produced_year = None, None
                if isPopular100List:
                    title = content[0]
                    produced_year = int(content[1][1:-1])
                else:
                    title = content[1]
                    produced_year = int(content[2][1:-1])
                    
                movie_title.append(title)

                ref = cell.find("a")
                url_link = urljoin(base_url, ref.get("href"))
                movie_link.append(url_link)

            if (cell.get("class") == ["ratingColumn", "imdbRating"]):
                content = list(filter((lambda x: len(x) > 0), cell.text.split("\n")))
                if (len(content) > 0):
                    IMDb_rating.append(float(content[0]))
                else:
                    IMDb_rating.append(None)
                
    return movie_title, movie_link, IMDb_rating

def getMovieList(list_name):
    assert(listInfo.get(list_name, None) != None)
    URL, chart_name = listInfo[list_name]
    soup = get_PageContent_from_URL(URL)
    table = get_element_with_attribute(soup, "data-caller-name", chart_name)[0]
    assert(table.name == "table")

    return listParsing(table, list_name == "Popular100")

if __name__ == "__main__":
    movie_title, movie_link, IMDb_rating = getMovieList("Popular100")
    for i, title in enumerate(movie_title):
        print(i + 1, title)

