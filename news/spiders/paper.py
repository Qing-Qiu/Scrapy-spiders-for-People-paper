import requests
import scrapy
import calendar

from news.items import NewsItem


class PaperSpider(scrapy.Spider):
    name = 'paper'
    allowed_domains = ['paper.people.com.cn']
    start_urls = ['http://paper.people.com.cn/rmrb/html/2021-01/01/'
                  'nw.D110000renmrb_20210101_1-01.htm']

    def parse(self, response):
        total = response.xpath("/html/body/div[@class='main w1000']/"
                               "div[@class='right right-main']/"
                               "div[@class='article-box']/div"
                               "[@class='article']/div[@id='ozoom']/p")
        title = response.xpath("/html/body/div[@class='main w1000']/"
                               "div[@class='right right-main']/"
                               "div[@class='article-box']/div"
                               "[@class='article']/h1")
        sub_title = response.xpath("/html/body/div[@class='main w1000']/"
                                   "div[@class='right right-main']/"
                                   "div[@class='article-box']/div"
                                   "[@class='article']/h2")

        paper_item = NewsItem()
        paper_item['title'] = title.xpath("./text()").extract()
        paper_item['sub_title'] = sub_title.xpath("./text()").extract()
        paper_item['article'] = total.xpath("./text()").extract()
        print(paper_item)

        next_ = response.xpath("/html/body/div[@class='main w1000']/"
                               "div[@class='right right-main']/"
                               "div[@class='article-box']/div"
                               "[@class='art-btn']/strong")
        next_page = next_.xpath("./a[2]/@href").extract()
        if next_page:
            next_page = next_page[0]
            temp = next_page[17:25]
            year = temp[0:4]
            month = temp[4:6]
            day = temp[6:8]
            date = year + "-" + month + "/" + day + "/"
            url_ = "http://paper.people.com.cn/rmrb/html/"
            new_url = url_ + date + next_page
            print(new_url)
            yield scrapy.Request(new_url, callback=self.parse)
        else:
            prev_page = next_.xpath("./a[1]/@href").extract()
            prev_page = prev_page[0]
            temp = prev_page[17:25]
            year = temp[0:4]
            month = temp[4:6]
            day = temp[6:8]
#            _year: str
#            _month: str
#            _day: str
            if calendar.mdays[int(month)] == int(day):
                if int(month) == 12:
                    _year = str(int(year) + 1)
                    _month = "01"
                    _day = "01"
                else:
                    _year = year
                    _month = str(int(month) + 1)
                    if int(_month) < 9:
                        _month = "0" + _month
                    _day = "01"
            else:
                _year = year
                _month = month
                _day = str(int(day) + 1)
                if int(day) < 9:
                    _day = "0" + _day
            temp = _year + _month + _day
            date = _year + "-" + _month + "/" + _day + "/"
            url_ = "http://paper.people.com.cn/rmrb/html/"
            new_url = url_ + date + "nw.D110000renmrb_" + temp + "_1-01.htm"
            print(new_url)
            yield scrapy.Request(new_url, callback=self.parse)
