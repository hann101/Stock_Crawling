import scrapy
from mystock.items import MystockItem


class MybotsSpider(scrapy.Spider):
    name = 'mybots'

    custom_settings = {'JOBDIR': 'crawl_mybots1'}
    allowed_domains = ['finance.yahoo.com/quote/005930.KS?p=005930.KS']
    start_urls = ['http://finance.yahoo.com/quote/005930.KS?p=005930.KS']

    def parse(self, response):
        stock_name = response.xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1/text()').extract()
        #해당 xpath에서 text형식만 추출할것이다.
        stock_price = response.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]/text()').extract()
        stock_range = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]/text()').extract()
        stock_volume = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span/text()').extract()
        #파싱 받을 내용들 

        items = []
        for row in zip(stock_name,stock_price,stock_range,stock_volume):
            # 변수의 갯수만큼 돌릴 것이다 -> 4번
            # zip으로 value값을 item['키 값']에 저장.
            item = MystockItem()
            #인스턴스화
            item['stock_name'] = row[0]
            #row 0번에 주식이름 파싱한 것을 대입한다.
            #stock_name(row[0])에서 받은 value를 item['name']라는 Key 값에 저장
            
            item['stock_price'] = row[1]
            # row 1번에 주식 가격 파싱한 것을 대입한다.
            item['stock_range'] = row[2]
            # row 2번에 주식 범위 파싱한 것을 대입한다.
            item['stock_volume'] = row[3]
            # row 3번에 주식 거래량 파싱한 것을 대입한다.

            yield item
            #item을 함수 바깥에 양보
            #setting을 통해 json으로 저장

