import re
import csv
import time
import scrapy
import os.path
import requests

from lxml import html
from scrapy.http import FormRequest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from scrapecentral.items import ScrapecentralItem


class RCSpider(scrapy.Spider):
    name = "rc"
    domain = "https://secure.remindercall.com"
    start_urls = ["https://secure.remindercall.com/login"]
    password_ = '6fx0o3QN%29o'
    login_ = '2m@doctormm.com'
    detail_field_set = ['Type', 'sound', 'Recipient', 'Name', 'Group', 'Appt.', 'Delivery', 'Duration', 'Tries/Status', 'Reply']

    def __init__(self):
        """
        Creating header names for the CSV file
        :param data: self
        :return:
        """
        self.filepath = '/home/sayone/projects/Scrapy/scrapecentral/scrapecentral/rc_data.csv'
        if os.path.exists(self.filepath) is False:
            with open('rc_data.csv', 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.detail_field_set)
                writer.writeheader()

    def parse(self, response):
        """
        Login, fetch data and write into CSV file
        :param data: response
        :return:
        """
        driver = webdriver.Chrome(executable_path=r'/home/sayone/Downloads/chromedriver')
        url = 'https://secure.remindercall.com/login'
        driver.get(url)
        time.sleep(2)
        log = driver.find_element_by_id('pageUsername')
        log.clear()
        log.send_keys(self.login_)

        passw = driver.find_element_by_id('pagePassword')
        passw.clear()
        passw.send_keys(self.password_, Keys.ENTER)
        time.sleep(5)

        driver.get('https://secure.remindercall.com')
        time.sleep(5)

        if 'Michael Morgenstern' in driver.page_source:

            table = driver.find_element_by_id('statsTable')
            last = table.find_elements_by_tag_name('tr')[-1]
            last.find_element_by_tag_name('a').click()
            time.sleep(2)

            scrape_table = driver.find_element_by_id('rStatsTable')
            tbody = scrape_table.find_element_by_tag_name('tbody')

            rows = tbody.find_elements_by_tag_name('tr')
            rows = [i.find_elements_by_tag_name('td') for i in rows]
            rows = [[i.text for i in y] for y in rows]

            rows = [[x.encode('UTF8') for x in row] for row in rows]
            rows = [[x.replace('null ', '') for x in row] for row in rows]

            data_list = []
            for row in rows:
                row = filter(None, row)
                data_list.append(row)

            for row in data_list:
                with open('rc_data.csv', 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=row)
                    writer.writeheader()

        else:
            print 'ERROR with login'


