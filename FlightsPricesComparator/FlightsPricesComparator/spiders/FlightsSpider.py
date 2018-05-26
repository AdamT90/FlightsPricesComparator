import scrapy
import time
from selenium import webdriver

class FLightsSpider(scrapy.Spider):
    name = "flightsRadar"

    def start_requests(self):
        urls = ['https://www.ryanair.com/pl/pl/']
        for url in urls:
            yield scrapy.Request(url=url,callback = self.parse)

    def parse(self, response):
        print(response)