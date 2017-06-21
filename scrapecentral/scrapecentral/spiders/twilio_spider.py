import re
import csv
import scrapy
import os.path
import requests
import subprocess

from collections import defaultdict

from lxml import html
from twilio.rest import Client
from scrapy.http import FormRequest
from scrapecentral.items import ScrapecentralItem


class TwilioSpider(scrapy.Spider):
    name = "twilio"
    domain = "https://www.twilio.com"
    start_urls = ["https://www.twilio.com/login"]
    password_ = '4r6&^jhg&U1234'
    login_ = 'Tester@medwiser.org'

    account_sid = "ACda10725b966b653d1fd4e8ee3bc4fa9c"
    auth_token = "b57924fb283d944aa79b424b6b86bafb"
    detail_field_set = ['Country code', 'Phone Number', 'National Format', 'Url', 'Caller Name', 'Caller Type', 'Type', 'Mobile Network Code', 'Mobile Country Code', 'Name']

    def __init__(self):
        """
        Creating header names for the CSV file
        :param data: self
        :return:
        """
        self.filepath = '/home/sayone/projects/Scrapy/scrapecentral/scrapecentral/twilio.csv'
        if os.path.exists(self.filepath) is False:
            with open('twilio.csv', 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.detail_field_set)
                writer.writeheader()

    def parse(self, response):
        """
        Fetch details of a specific number and save it into CSV
        :param data: response
        :return:
        """
        client = Client(self.account_sid, self.auth_token)
        number = client.lookups.phone_numbers("+1415-701-2218").fetch(type=["carrier", "caller-name"],)
        # number2 = client.lookups.phone_numbers("+1415-701-2311").fetch(type="caller-name")

        country_code = number.country_code
        phone_number = number.phone_number
        national_format = number.national_format
        url = number.url

        caller_name = number.caller_name['caller_name']
        caller_type = number.caller_name['caller_type']
        error_code = number.caller_name["error_code"]

        type = number.carrier["type"]
        error_code = number.carrier["error_code"]
        mobile_network_code = number.carrier["mobile_network_code"]
        mobile_country_code = number.carrier["mobile_country_code"]
        name = number.carrier["name"]

        data = [country_code, phone_number, national_format, url, caller_name, caller_type, type, mobile_network_code, mobile_country_code, name]
        with open('twilio.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data)
            writer.writeheader()
