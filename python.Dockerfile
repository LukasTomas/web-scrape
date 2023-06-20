FROM python

WORKDIR /app

COPY src/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/ .

CMD cd srealityscraper; scrapy crawl sreality; cd ..; python3 server.py