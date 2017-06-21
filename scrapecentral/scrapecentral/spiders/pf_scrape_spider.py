import re
import csv
import json
import time
import scrapy
import poplib
import logging
import os.path
import requests
from datetime import datetime, timedelta

from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from scrapy.http import FormRequest
from scrapecentral.items import ScrapecentralItem


class PFScrapeSpider(scrapy.Spider):
    name = "pf_scrape"
    domain = "http://www.practicefusion.com/"
    start_urls = ["https://static.practicefusion.com/apps/ehr/?c=1385407302#/login"]
    password_ = 'pA142*2@'
    login_ = '2m@doctormm.com'

    # gmail account details
    server = "pop.gmail.com"
    user  = "Tester@medwiser.org"
    password = "4r6&^jhg&U"

    detail_field_set = ['APPOINTMENT TYPE', 'PATIENT/DOB', 'FACILITY', 'STATUS', 'DATE/TIME', 'SEEN BY PROVIDER']

    def __init__(self):
        """
        Creating header names for the CSV file
        :param data: self
        :return:
        """
        self.filepath = '/home/sayone/projects/Scrapy/scrapecentral/scrapecentral/PF_scrape.csv'
        if os.path.exists(self.filepath) is False:
            with open('PF_scrape.csv', 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.detail_field_set)
                writer.writeheader()

    def parse(self, response):
        """
        Login, fetch data and write into CSV
        :param data: response
        :return:
        """
        driver = webdriver.Chrome(executable_path=r'/home/sayone/Downloads/chromedriver')

        url = 'https://static.practicefusion.com/apps/ehr/?c=1385407302#/login'
        driver.get(url)
        time.sleep(2)
        log = driver.find_element_by_id('inputUsername')
        log.clear()
        log.send_keys(self.login_)

        passw = driver.find_element_by_id('inputPswd')
        passw.clear()
        passw.send_keys(self.password_, Keys.ENTER)
        time.sleep(5)

        if "We don't recognize this browser" in driver.page_source:
            print 'its Security check......'

            driver.find_element_by_xpath('.//button[@id="sendCallButton"]').click()
            time.sleep(6)

            #fetch OTP from mail
            otp = self.parse_otp_from_mail()

            time.sleep(2)
            log = driver.find_element_by_id('code')
            log.clear()
            log.send_keys(otp, Keys.ENTER)
            time.sleep(3)

            driver.find_element_by_link_text("Reports").click();
            time.sleep(2)

            driver.find_element_by_link_text("Appointment report").click();
            today = datetime.today()
            before = today - timedelta(days=7)
            before = before.strftime('%m/%d/%Y')

            after = today + timedelta(days=30)
            after = after.strftime('%m/%d/%Y')
            time.sleep(4)

            driver.find_element_by_id('fromDatePicker').clear()
            driver.find_element_by_id('fromDatePicker').send_keys(before)

            driver.find_element_by_id('toDatePicker').clear()
            driver.find_element_by_id('toDatePicker').send_keys(after)

            driver.find_element_by_xpath('//button[text() = "Run report"]').click()

            while True:
                time.sleep(2)
                table = driver.find_element_by_class_name('data-grid-table-container')
                rows = table.find_elements_by_tag_name('tr')
                rows = [i.find_elements_by_tag_name('td') for i in rows]
                rows = [[i.text for i in y] for y in rows]
                rows.remove([])

                for row in rows:
                    with open('PF_scrape.csv', 'a') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=row)
                        writer.writeheader()

                but = driver.find_element_by_class_name('pagination-buttons')
                try:
                    but.find_elements_by_tag_name('button')[-1].click()
                except:
                    print('no more pages')
                    break

            print('DONE')
            driver.quit()
            # return True

    def parse_otp_from_mail(self):
        """
        Fetch otp details from gmail inbox
        :param data: self
        :return:
        """
        logging.debug('connecting to ' + self.server)
        server = poplib.POP3_SSL(self.server)
        #server = poplib.POP3(SERVER)

        # login
        logging.debug('logging in')
        server.user(self.user)
        server.pass_(self.password)
        mail_count = server.stat()[0],

        ## fetch the top mail
        latest_email = server.retr(mail_count)
        mail_text_data = str(latest_email)
        otp = re.findall(r'Your code is: (.+?). T', mail_text_data, re.DOTALL)
        if len(otp) == 2:
            otp = otp[0]
        else:
            otp = otp

        return otp
