# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.crawler import Crawler
from twisted.enterprise import adbapi


class LieyunPipeline:
    def __init__(self, mysql_config):
        # 异步mysql
        self.db = adbapi.ConnectionPool(
            mysql_config['DRIVER'],
            host=mysql_config['HOST'],
            port=mysql_config['PORT'],
            user=mysql_config['USER'],
            password=mysql_config['PASSWORD'],
            db=mysql_config['DATABASE'],
            charset='utf8'
        )
        super().__init__()

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        # 调用这个方法获取pipline对象
        mysql_config = crawler.settings['MYSQL_CONFIG']
        return cls(mysql_config)

    def process_item(self, item, spider):
        result = self.db.runInteraction(self.insert_item, item)
        result.addErrback(self.insert_error)
        return item

    def insert_item(self, cursor, item):
        sql = "insert into archives(title, author, pub_time, content, origin) " \
                        "values(%s, %s, %s, %s, %s)"
        args = (item['title'], item['author'], item['pub_time'], item['content'], item['origin'])
        cursor.execute(sql, args)

    def insert_error(self, failure):
        print('=' * 30)
        print(failure)
        print('=' * 30)

    def close_spider(self, spider):
        self.db.close()
