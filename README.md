# IMDb_crawler
Automatically grabs movie and rating data from IMDb.

This crawler can grab ratings of movies from three lists (**Top250**/**Lowest100**/**Popular100**).

For each movie, the RatingCrawler can grab the rating information (including vote distribution, weighted average rating calculated by IMDb, arithmetic mean rating, median rating) of different groups (e.g. Female/Male group, group divided by age, top 1000 voters, US/Non-US group).

The crawler will dump the rating data of movies into a json file.
