# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class AmazonImagesPipeline(object):
    def open_spider(self, spider):
        spider.logger.info("Connect to database")
        spider.connection = sqlite3.connect("urldb.sqlite3")

        try:
            cursor = spider.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS urls(
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    url         VARCHAR(500),
                    timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP,
                    title       VARCHAR(500),
                    seller_rank INTEGER
                )
            """)
        finally:
            cursor.close()

    def close_spider(self, spider):
        spider.connection.close()

    def process_item(self, item, spider):
        if item['data']:
            file_name = "images/{}.jpg".format(item['name'])

            with open(file_name, "wb") as buff:
                buff.write(item['data'])

            # If everything is allright with the item,
            # store url to database.
            try:
                cursor = spider.connection.cursor()
                cursor.execute("""
                    INSERT INTO urls(url, title, seller_rank) VALUES(?, ?, ?)
                """, (item['url'], item['title'], item['seller_rank']))

            finally:
                spider.connection.commit()
                cursor.close()

            return "ok"

        else:
            return "err"
