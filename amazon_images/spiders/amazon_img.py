# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from amazon_images import tools


class AmazonImgSpider(scrapy.Spider):
    name = 'amazon_img'
    allowed_domains = ["amazon.com", "ssl-images-amazon.com"]

    def start_requests(self):
        # TODO: handle file absense.
        try:
            with open("urls.txt") as urls_buff:
                for url in urls_buff:
                    url = url.strip()
                    if not tools.url_is_scraped(self.connection, url):
                        yield Request(url, callback=self.parse_page)
                    else:
                        self.logger.info("Skipping scraped url: [{}]".format(url))
        except IOError:
            print("\n\n\nAdd your urls to urls.txt\n\n\n")

    def parse_page(self, response):
        img_xp = "//div[@id='imgTagWrapperId']/img/@data-old-hires"
        try:
            image_url = response.xpath(img_xp).extract()[0]
            resp_name = response.url.split('/')[-1]
            yield Request(image_url, callback=self.fetch_image,
                          meta={'name': resp_name, 'url': response.url})

        except IndexError:
            yield dict(image=None)

    def fetch_image(self, response):
        yield dict(data=response.body,
                   name=response.meta['name'],
                   url=response.meta['url'])
