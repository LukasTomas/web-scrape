import scrapy


class SrealitySpider(scrapy.Spider):
    name = "sreality"
    allowed_domains = ["sreality.cz", "d18-a.sdn.cz"]

    n_flats = 500
    start_urls = ["https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=" + str(n_flats)]

    def parse(self, response):
        estates = response.json()['_embedded']['estates']
        self.log(f'Got {len(estates)} flats')


        for estate in estates:
            item = {
                'name': estate['name'],
                'image_urls': [ estate['_links']['image_middle2'][0]['href'] ]
            }

            yield scrapy.Request(estate['_links']['image_middle2'][0]['href'], callback=self.parseImages,  meta={'item': item})

    def parseImages(self, response):
        item = response.meta['item']
        item['image_bin'] = response.body
        yield item