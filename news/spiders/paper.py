import requests
import scrapy
import calendar

from news.items import NewsItem


class PaperSpider(scrapy.Spider):
    name = 'paper'
    allowed_domains = ['paper.people.com.cn']
    start_urls = ['http://paper.people.com.cn/rmrb/html/2022-01/01/nw.D110000renmrb_20220101_1-04.htm']

    def parse(self, response):
        content = response.xpath("/html/body/div[@class='main w1000']/"
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
        cite_title = response.xpath("/html/body/div[@class='main w1000']/"
                                    "div[@class='right right-main']/"
                                    "div[@class='article-box']/div"
                                    "[@class='article']/h3")
        paper_item = NewsItem()
        paper_item['title'] = title.xpath("./text()").extract()
        paper_item['sub_title'] = sub_title.xpath("./text()").extract()
        paper_item['cite_title'] = cite_title.xpath("./text()").extract()
        paper_item['content'] = content.xpath("./text()").extract()
        paper_item['content'] = "".join(paper_item['content'])
        paper_item['content'] = paper_item['content'].replace(" ", "")
        paper_item['url'] = response.request.url
        button_first = response.xpath("/html/body/div[@class='main w1000']/"
                                      "div[@class='right right-main']/"
                                      "div[@class='article-box']/div"
                                      "[@class='art-btn']/strong"
                                      "/a[1]/@href").extract()
        button_second = response.xpath("/html/body/div[@class='main w1000']/"
                                       "div[@class='right right-main']/"
                                       "div[@class='article-box']/div"
                                       "[@class='art-btn']/strong"
                                       "/a[2]/@href").extract()
        judger = response.xpath("/html/body/div[@class='main w1000']/"
                                "div[@class='right right-main']/div["
                                "@class='article-box']/div[@class='ar"
                                "t-btn']/strong/a[@class='preart'][1]/"
                                "span/text()").extract()
        judger = str(judger)
        judger.replace(" ", "")

        if button_second or (button_first and ("下一篇" in judger)):
            if button_second:
                next_page = button_second[0]
            else:
                next_page = button_first[0]
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
            cur_page = str(response.request.url)
            temp = cur_page[65:73]
            year = temp[0:4]
            month = temp[4:6]
            day = temp[6:8]
            if calendar.mdays[int(month)] == int(day):
                if int(month) == 12:
                    _year = str(int(year) + 1)
                    _month = "01"
                    _day = "01"
                else:
                    _year = year
                    _month = str(int(month) + 1)
                    if int(_month) <= 9:
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
            new_url = url_ + date + "nw.D110000renmrb_" + temp + "_1-04.htm"
            print(new_url)
            yield scrapy.Request(new_url, callback=self.parse)
        yield paper_item
