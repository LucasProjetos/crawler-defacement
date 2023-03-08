FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD [ "python3", "./go-spider.py" ]
CMD [ "scrapy", "crawl", "defacementcrawler.py", "-s", "JOBDIR=jobs/mycrawler" ]
