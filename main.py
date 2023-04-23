from TitleCrawler import getMovieList
from RatingCrawler import get_rating_by_groups_from_movieHomepage
import json

list = ["Top250", "Lowest100", "Popular100"]

list_name = "Top250"

movieTitles, movieLinks, IMDbRatings = getMovieList(list_name)
data = {}
for id, (title, link) in enumerate(zip(movieTitles, movieLinks)):
    print("Loading the rating data of Movie {index}: {title} ...".format(index = id + 1, title = title))
    data[id + 1] = (title, get_rating_by_groups_from_movieHomepage(link)) 

content = json.dumps(data)
file = open("{list_name}.json".format(list_name = list_name), "w")
file.write(content)
file.close()

