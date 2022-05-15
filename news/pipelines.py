# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql


class NewsPipeline(object):
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.connect(host='localhost', port=3306,
                                    db='paper_db', user='root',
                                    passwd='root', charset='utf8')

    def process_item(self, item, spider):
        if item['title'] and item['sub_title'] and item['cite_title']:
            title = str(item['cite_title'][0]) + ':' + str(item['title'][0]) + ':' + str(item['sub_title'][0])
        elif item['title'] and item['sub_title']:
            title = str(item['title'][0]) + ':' + str(item['sub_title'][0])
        elif item['cite_title'] and item['title']:
            title = str(item['cite_title'][0]) + ':' + str(item['title'][0])
        elif item['title']:
            title = str(item['title'][0])
        values = (title, str(item['url']), str(item['content']))
        sql = 'INSERT INTO doc_raws(title,url,content) VALUES(%s,%s,%s)'
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql, values)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.commit()
        self.conn.close()
