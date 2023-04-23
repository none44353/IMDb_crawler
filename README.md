# IMDb爬虫
自动从IMDb抓取电影和评分数据。

此爬虫可以从IMDb列表（**Top250**/**Lowest100**/**Popular100**）中抓取电影和其评分。

对于每部电影，评分爬虫可以抓取不同群体（例如男性/女性群体、按年龄分组、前1000名评审、美国/非美国用户）的评分信息（包括投票分布、IMDb计算的加权平均分、算术平均分、中位数评分）。

该爬虫将电影的评分数据转储到json文件中。
# IMDb_crawler
Automatically grabs movie and rating data from IMDb.

This crawler can crawl movies and their ratings from IMDb lists (**Top250**/**Lowest100**/**Popular100**).

For each movie, the RatingCrawler can grab the rating information (including vote distribution, weighted average rating calculated by IMDb, arithmetic mean rating, median rating) of different groups (e.g. Female/Male group, group divided by age, top 1000 voters, US/Non-US group).

The crawler will dump the rating data of movies into a json file.

## 使用方法
- 安装依赖库
```pip install -r requirements.txt```

- 运行主程序
```python main.py```

## Usage
- Install dependencies by running: ```pip install -r requirements.txt```
- Run the main program by executing: ```python main.py```

## 为什么这个爬虫跑得很慢？
在抓取一部电影的评分页面时，根据爬虫提供的URL，IMDb服务器可能会返回两种不同的HTML内容。其中一种是我的解析器可以分析的，另一种不是。针对这个问题，该爬虫采用的策略是：停顿一段时间（waiting_time）后重新请求页面。这导致该爬虫跑得很慢。如果您有更好的方法解决这个问题，请与我联系。

## Why is this web crawler running slowly?
When the crawler is trying to grab the rating page of a movie based on the provided URL, IMDb server may return two different types of HTML content. One type can be parsed by the crawler's parser, while the other cannot. To handle this issue, the crawler adopts a strategy of pausing for a certain amount of time (waiting_time) and then re-requesting the page. This causes the crawler to run slowly. If you have a better solution to this problem, please contact me.
