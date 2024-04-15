# News Scraper
## Python / Scrapy / Docker
![alt text](imgs/terminal.png)

![alt text](imgs/workbench.png)



## A simple Scrapy Script that captures news articles and saves them to a DB
### How it works





The function of this crawler is to scrape the local news page of CBS News Ex. 
<br> <br>
www.cbsnews.com/{your-state}/local-news/

When the docker comppose file is used, 2 containers start. One container will run a MYSQL Docker Image. The other container is a Python Scrapy Image. 

Once the compose file finishes a MySQL Database will start running on Localhost. 

Using Cron tasks we can then run the Python Image at any interval. (1 hour works well depending on location)

