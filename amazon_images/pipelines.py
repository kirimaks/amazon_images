# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AmazonImagesPipeline(object):
    def process_item(self, item, spider):
        file_name = "images/{}.jpg".format(item['name'])

        with open(file_name, "wb") as buff:
            buff.write(item['data'])

        return "ok"
