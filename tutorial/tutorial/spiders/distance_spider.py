import scrapy
import logging
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
    def start_requests(self):
        cwd = os.getcwd()
        workbook = load_workbook(cwd + '/part1_getting_url.xlsx')
        first_sheet = workbook.get_sheet_names()[0]
        worksheet = workbook.get_sheet_by_name(first_sheet)
        urls = []
        for index,row in enumerate(worksheet.iter_rows()):
            if index != 0:
                fromPostcode = row[0].internal_value
                toPostcode = row[1].internal_value
                url = "http://distancecalculator.globefeed.com/Singapore_Distance_Result.asp?fromplace={0}&toplace={1}".format(fromPostcode,toPostcode)
                urls.append(url)
        print urls
        for url in urls:
            yield SplashRequest(url, self.parse)

    def parse(self, response):
        # open_in_browser(response)
        drivingDistance = response.css('span#drvDistance.badge').xpath('text()')[0].extract()
        yield {
            'distance': drivingDistance
        }
        # yield {
        #     'propertyTitle': propertyTitle,
        #     'propertyType': propertyType,
        #     'propertyLocation': propertyLocation,
        #     'propertySize': propertySize,
        #     'propertyFeature': propertyFeature,
        #     'propertyCost': propertyCost,
        #     'propertyContactNumber': propertyContactNumber,
        #     'propertyContactPerson': propertyContactPerson,
        #     'propertyUpdateTime': propertyUpdateTime,
        # }
        # if len(response.headers.getlist('Set-Cookie')) > 0:
        #     fakeCookie['PHPSESSID2'] = response.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
        # if len(response.headers.getlist('Set-Cookie')) > 1:
        #     fakeCookie['sixpack_client_id'] = response.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[1]
