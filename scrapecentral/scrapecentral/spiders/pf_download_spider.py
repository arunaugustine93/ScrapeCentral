import re
import json
import time
import scrapy
import poplib
import logging
import requests
import string, random
import StringIO, rfc822

from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from scrapy.http import FormRequest
from scrapecentral.items import ScrapecentralItem


class PFDownloadSpider(scrapy.Spider):
    name = "pf_download"
    domain = "http://www.practicefusion.com/"
    start_urls = ["https://static.practicefusion.com/apps/ehr/?c=1385407302#/login"]
    password_ = 'pA142*2@'
    login_ = '2m@doctormm.com'

    # gmail account details
    server = "pop.gmail.com"
    user  = "Tester@medwiser.org"
    password = "4r6&^jhg&U"

    def parse(self, response):
        """
        Login and export the CSV file
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
            time.sleep(1)

            driver.find_element_by_link_text("Patient lists report").click();
            driver.find_element_by_xpath('//span[text() = "Start a new query..."]').click()
            driver.find_element_by_xpath('//a[text() = "Age"]').click()
            driver.find_element_by_xpath('//a[text() = "="]').click()
            driver.find_element_by_xpath('//a[text() = ">="]').click()

            driver.find_element_by_tag_name('input').send_keys('0')
            driver.find_element_by_xpath('//button[text() = "Run Report"]').click()
            time.sleep(2)
            driver.find_element_by_xpath('//button[text() = "Export CSV"]').click()
            time.sleep(10)

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