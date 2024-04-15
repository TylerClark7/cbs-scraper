FROM python:3.12.2

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY cbs_src /app/
WORKDIR /app/cbs_src/cbs

CMD [ "scrapy", "crawl", "articles_sql"]


