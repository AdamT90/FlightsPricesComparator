import scrapy
from scrapy.http import TextResponse
import time
from selenium import webdriver


class FLightsSpider(scrapy.Spider):
    name = "flightsCatcher_Ryanair"

    start_urls = ['https://www.ryanair.com/pl/pl/']

    btn_close_cookie = '//*[@id="home"]/cookie-pop-up/div/div[2]/core-icon'
    continue_but_loc = '''//*[@id="search-container"]/div[1]/div/form/div[4]/button[1]'''
    agree_terms_loc = '''//*[@id="search-container"]/div[1]/div/div/div[2]/div/label'''
    lets_fly_loc = '''//*[@id="search-container"]/div[1]/div/form/div[4]/button[2]'''

    from_textfield_str = \
        '''//*[@id="search-container"]/div[1]/div/form/div[2]/div/div/div[1]/div[2]/div[2]/div/div[1]/input'''
    to_textfield_str = \
        '''//*[@id="search-container"]/div[1]/div/form/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/input'''

    from_day = '''//*[@id="row-dates-pax"]/div[1]/div/div[1]/div/div[2]/div[2]/div/input[1]'''
    from_month = '''//*[@id="row-dates-pax"]/div[1]/div/div[1]/div/div[2]/div[2]/div/input[2]'''
    from_year = '''//*[@id="row-dates-pax"]/div[1]/div/div[1]/div/div[2]/div[2]/div/input[3]'''

    to_day = '''//*[@id="row-dates-pax"]/div[1]/div/div[2]/div/div[2]/div[2]/div/input[1]'''
    to_month = '''//*[@id="row-dates-pax"]/div[1]/div/div[2]/div/div[2]/div[2]/div/input[2]'''
    to_year = '''//*[@id="row-dates-pax"]/div[1]/div/div[2]/div/div[2]/div[2]/div/input[3]'''

    flights_table_path = '''//*[@id="outbound"]/form/div[3]/div/flights-table/div'''


    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Chrome('./chromedriver')
        #self.output_filename = 'ryanair_res.html'
        self.output_filename = 'ryanair_res2.html'
        self.there_date = time.strptime("1 Jun 18", "%d %b %y")
        self.back_again_date = time.strptime("10 Jun 18", "%d %b %y")

    #def start_requests(self):
    #    for url in self.start_urls:
    #        yield scrapy.Request(url=url, callback=self.parse)

    def fill_field(self, _address, _value):
        page_element = self.driver.find_element_by_xpath(_address)
        page_element.clear()
        page_element.send_keys(_value)
        page_element.submit()

    def parse(self, response):
        self.driver.set_window_size(1024, 768)
        self.driver.maximize_window()
        self.driver.get(response.url)

        time.sleep(10)

        btn_close_cookie_po = self.driver.find_element_by_xpath(self.btn_close_cookie)
        btn_close_cookie_po.click()

        self.fill_field(self.from_textfield_str, "Warszawa-Modlin")
        #from_textfield_po = self.driver.find_element_by_xpath(self.from_textfield_str)
        #from_textfield_po.clear()
        #from_textfield_po.send_keys("Warszawa-Modlin")
        #from_textfield_po.submit()

        to_textfield_po = self.driver.find_element_by_xpath(self.to_textfield_str)
        to_textfield_po.clear()
        to_textfield_po.send_keys("Londyn-Stansted")
        to_textfield_po.submit()

        #self.driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")

        continue_but_loc_po = self.driver.find_element_by_xpath(self.continue_but_loc)
        continue_but_loc_po.click()

        self.log("TESTING LOGS")
        time.sleep(5)

        self.fill_field(self.from_day, self.there_date.tm_mday)
        self.fill_field(self.from_month, self.there_date.tm_mon)
        self.fill_field(self.from_year, self.there_date.tm_year)

        self.fill_field(self.to_day, self.back_again_date.tm_mday)
        self.fill_field(self.to_month, self.back_again_date.tm_mon)
        self.fill_field(self.to_year, self.back_again_date.tm_year)

        time.sleep(5)

        agree_terms_po = self.driver.find_element_by_xpath(self.agree_terms_loc)
        agree_terms_po.click()
        lets_fly_po = self.driver.find_element_by_xpath(self.lets_fly_loc)
        lets_fly_po.click()
        time.sleep(30)
        self.driver.save_screenshot('./result.jpg')
        resultEl = self.driver.find_element_by_xpath(self.flights_table_path)
        res = resultEl.get_attribute('innerHTML')
        text_html = self.driver.page_source.encode('utf-8')
        #print(text_html)
        with open(self.output_filename,'a') as outf:
            outf.write('<date_there_input>' + str(self.there_date.tm_mday) + ' ' + str(self.there_date.tm_mon) + ' ' + str(self.there_date.tm_year) + '</date_there_input>')
            outf.write('<date_back_again_input>' + str(self.back_again_date.tm_mday) + ' ' + str(self.back_again_date.tm_mon) + ' ' + str(self.back_again_date.tm_year) + '</date_back_again_input>')
            outf.write(str(res))
            #outf.write(str(text_html))

        #resp_for_scrapy = TextResponse('none', 200, {}, text_html, [], None)
        #test_out = resp_for_scrapy.xpath('''//*[@id="enclosed-links"]/text()''').extract_first()
        #tabl = resp_for_scrapy.xpath(self.flights_table_path).extract()
        #print("TRALALALALALALALALA " + test_out)
        #print("TABL " + str(tabl))
        #with open('tabl.html','w') as outf:
        #    outf.write(str(tabl))
        self.driver.quit()
