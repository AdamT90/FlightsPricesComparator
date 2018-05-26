import scrapy
import time
from selenium import webdriver


class FLightsSpider(scrapy.Spider):
    name = "flightsRadar2"

    start_urls = ['https://www.ryanair.com/pl/pl/']

    btn_close_cookie = '//*[@id="home"]/cookie-pop-up/div/div[2]/core-icon'
    btn_continue = '''//*[@id="search-container"]/div[1]/div/form/div[4]/button[1]'''

    from_textfield_str = '''//*[@id="search-container"]/div[1]/div/form/div[2]/div/div/div[1]/div[2]/div[2]/div/div[1]/input'''
    to_textfield_str = '''//*[@id="search-container"]/div[1]/div/form/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/input'''

    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Chrome('./chromedriver')

    #def start_requests(self):
    #    for url in self.start_urls:
    #        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.driver.set_window_size(1024, 768)
        self.driver.maximize_window()
        self.driver.get(response.url)
        time.sleep(10)
        btn_close_cookie_po = self.driver.find_element_by_xpath(self.btn_close_cookie)
        btn_close_cookie_po.click()
        from_textfield = self.driver.find_element_by_xpath(self.from_textfield_str)
        from_textfield.clear()
        from_textfield.send_keys("Warszawa-Modlin")
        from_textfield.submit()
        to_textfield = self.driver.find_element_by_xpath(self.to_textfield_str)
        to_textfield.clear()
        to_textfield.send_keys("Londyn-Stansted")
        to_textfield.submit()
        #cont_but = self.driver.find_element_by_xpath(self.btn_continue)
        #cont_but.click()
        time.sleep(5)
        self.driver.quit()
