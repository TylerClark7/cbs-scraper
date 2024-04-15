import scrapy
from cbs.items import CbsItem

class NewsSpider(scrapy.Spider):

    name = "articles_sql"
    start_urls = [
        "https://www.cbsnews.com/minnesota/local-news/"     #Starting url
    ]

    def parse(self, response):
        #Gets all the article URLSs in the page along with Article Title and Article Description
        article_list =  response.xpath('//*[@id="component-minnesota-news-topic-door-river"]/div[2]/article')
        for index, article in enumerate(article_list):

            article_title =  article.css("h4::text").get().strip()
            description = article.css("p::text").get().strip()
            article_url = article.css("a::attr(href)").get().strip()



            yield scrapy.Request(article_url, callback=self.parse_article, meta={'index':index, 'article_title': article_title, 'description': description, 'url': article_url})
    
    def parse_article(self,response):
        #Crawls actual article webpages. Captures all the text in each paragraph
        new_article = CbsItem()
        
        new_article['title'] = response.meta['article_title']
        new_article["url"] = response.meta['url']
        new_article["description"] = response.meta['description']
        new_article["publish_date"] = response.xpath("//*[@id='article-header']/header/div[2]/p[2]/time//text()").get()
        content = response.xpath("//*[@id='article-0']/section/p//text()").getall() 
     
        new_article ['content'] = ''.join(text.strip() for text in content)

        yield new_article
        

