import scrapy
import logging
import csv
import os
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from scrapy_splash import SplashRequest
from openpyxl import load_workbook

fakeHeader={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-GB,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2,zh-TW;q=0.2,nb;q=0.2",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    'Cache-Control': 'max-age=0',
    'Referer': 'distancecalculator.globefeed.com',
    'Host': 'distancecalculator.globefeed.com',
    'Upgrade-Insecure-Requests': 1,
}

class DistanceSpider(scrapy.Spider):
    name = "distance"
    indexNumber = 0
    def start_requests(self):
        toPostcodeList = []
        toAddress = []
        cwd = os.getcwd()
        with open(cwd + '/postcode.csv', 'rU') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                toAddress.append(row[0])
                toPostcodeList.append(row[1])

        # workbook = load_workbook(cwd + '/part1_getting_url.xlsx')
        # first_sheet = workbook.get_sheet_names()[0]
        # worksheet = workbook.get_sheet_by_name(first_sheet)
        urls = []
        accumulateNumber = -100
        for postcode in toPostcodeList:
                fromPostcode = 257717
                toPostcode = postcode
                if toPostcode == '0':
                    toPostcode = accumulateNumber
                    accumulateNumber += 1
                url = "http://distancecalculator.globefeed.com/Singapore_Distance_Result.asp?fromplace={0}&toplace={1}".format(fromPostcode,toPostcode)
                urls.append(url)
        for url in urls:
            print url
            yield SplashRequest(url,self.parse,args={'wait': 10})

    def parse(self, response):
        # open_in_browser(response)
        drivingDistance = '-1 km'
        if len(response.css('span#drvDistance.badge').xpath('text()')) >= 1:
            drivingDistance = response.css('span#drvDistance.badge').xpath('text()')[0].extract()
        self.indexNumber += 1
        yield {
            'index': self.indexNumber,
            'url': response.url,
            'distance': drivingDistance
        }
