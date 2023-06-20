from itemadapter import ItemAdapter

import psycopg2
import scrapy

import time

class SrealityscraperPipeline(object):

    def __init__(self):
        self.conn = psycopg2.connect(database="my_db",
                    host="database",
                    user="root",
                    password="pass",
                    port="5432")
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        query = """INSERT INTO estates (name, image) VALUES (%s, %s);"""
        self.cursor.execute(query, [item['name'], item['image_bin']])
        
        self.conn.commit()

        return item
    

