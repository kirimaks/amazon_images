# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class AmazonImgSpider(scrapy.Spider):
    name = 'amazon_img'
    allowed_domains = ["amazon.com", "ssl-images-amazon.com"]

    images_urls = [
        'https://www.amazon.com/dp/B01981MRAW',
        'https://www.amazon.com/dp/B00CUWPVGY',
        'https://www.amazon.com/dp/B0186E1K2S',
        'https://www.amazon.com/dp/B01GW5F2UY',
        'https://www.amazon.com/dp/B0085N9CYE',
        'https://www.amazon.com/dp/B016019XOQ',
        'https://www.amazon.com/dp/B00XD00AO0',
        'https://www.amazon.com/dp/B000AZ4ZLU',
        'https://www.amazon.com/dp/B017V8XOL0',
        'https://www.amazon.com/dp/B01K35XOM2',
    ]

    def start_requests(self):
        for url in self.images_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        img_xp = "//div[@id='imgTagWrapperId']/img/@data-old-hires"
        try:
            image_url = response.xpath(img_xp).extract()[0]
            resp_name = response.url.split('/')[-1]
            yield Request(image_url, callback=self.fetch_image,
                          meta={'name': resp_name})

        except IndexError:
            yield dict(image=None)

    def fetch_image(self, response):
        yield dict(data=response.body,
                   name=response.meta['name'])
