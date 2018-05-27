import scrapy


class LocalSpider(scrapy.Spider):
    name = "htmlParser2"

    start_urls = ['''./ryanair_res2.html''']

    def parse(self, response):
        print("QWERTYUIOP///")
        test = response.xpath('''/html/body/date_there_input''').extract()
        print(test)