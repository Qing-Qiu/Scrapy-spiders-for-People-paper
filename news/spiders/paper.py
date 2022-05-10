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
        # for items in total:
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
            print(next_page)
            temp = next_page[17:25]
            date = temp[0:4]+"-"+temp[4:6]+"/"+temp[6:8]+"/"
            url_ = "http://paper.people.com.cn/rmrb/html/"
            new_url = url_ + date + next_page
            print(new_url)
            yield scrapy.Request(url_ + date + next_page, callback=self.parse)
        else:
            pass
        next_edit = 0
