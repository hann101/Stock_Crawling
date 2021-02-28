# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

#PIPE라인은 데이터베이스와 scrapy를 연결시켜준다. Scrapy로 받은 정보를 DB에 저장하는 역할을 한다. 

from itemadapter import ItemAdapter
import pymysql


class MystockPipeline:


    def __init__(self):
        self.setupDBConnect()
        #setupDBConnect를 초기화 단계에서 실행하겠다.
        self.createTable()
        #createTable을 초기화 단계에서 실행하겠다.


    def setupDBConnect(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root',password='123',db='mydb',charset='utf8',port=3306)
        self.cur = self.conn.cursor()
        print("-----------------DB Connected-------------------")



    def createTable(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS my_stock(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            price VARCHAR(100),
            volume VARCHAR(100),
            d_range VARCHAR(100),
            created_at DATETIME DEFAULT NOW()
        )''')
        print("-----------------Table creadted-------------------")

    def process_item(self, item, spider):
        self.storeInDb(item)
        return item


    def storeInDb(self, item):
        print("---------------",item,"----------------------")

        name = item.get('stock_name','').strip()
        #strip -> 앞뒤의 화이트 스트립을 제거해준다.
        #mybots에서 돌려받은 item 리스트의 row값을 받고 있다
        price = item.get('stock_price','').strip()
        volume = item.get('stock_volume','').strip()
        d_range = item.get('stock_range','').strip()
        #이하동문

        sql = "INSERT INTO my_stock(name,price,volume,d_range) VALUES(%s,%s,%s,%s)"
        self.cur.execute(sql, (name, price, volume, d_range))
        #위에서 받은 내용 db에 전달
        self.conn.commit()






        

        