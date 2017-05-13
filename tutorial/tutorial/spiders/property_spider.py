import scrapy
import logging
import random
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
fakeCookie = {
    'D_HID': 'Xw6WFpq9Be9whbrh5M/hrpwFUPrhhYVlRYoAXNVZeGk',
    'D_IID': '4C9B4B86-2E25-3C3D-8879-2ACABFE21001',
    'D_PID': '3FA36A85-B734-3C42-AAE2-4B569801AC4B',
    'D_SID': '42.60.131.145:TA6tOjTHjRb3KFycgUdw5svXo03A5XlWLM7k5Gyo8GU',
    'D_UID': '3C3CB9E5-42B5-39FD-B80F-00784D2FB3B9',
    'D_ZID': 'FD12B78C-947D-3B57-9CB6-957EFF6F52F8',
    'D_ZUID': 'AB483643-11C6-3719-AB6D-ABAE7FC0DCF6',
}
fakeHeader={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-GB,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2,zh-TW;q=0.2,nb;q=0.2",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    'Cache-Control': 'max-age=0',
    "Referer": "http://www.propertyguru.com/",
    'Host': 'www.propertyguru.com.sg',
    'Upgrade-Insecure-Requests': 1,
}
currentPage = 1

class PropertySpider(scrapy.Spider):
    name = "properties"
    handle_httpstatus_list = [405]
    baseUrl = "http://www.propertyguru.com.sg/distil_identify_cookie.html?d_ref=/"
    rentBaseUrl = "singapore-property-listing/property-for-rent?"
    def start_requests(self):
        global fakeCookie
        global fakeHeader
        location = 'DT14+Bugis+MRT+Station'
        bedRoom = '3'
        minPrice = '3000'
        maxPrice = '5000'
        distance = '2'
        parameter = "MRT_STATION=8107&center_lat=1.2989361886515&center_long=103.8569355011&limit=300&market=residential&freetext={0}&minprice={1}&maxprice={2}&beds%5B%5D={3}&distance={4}".format(location, minPrice, maxPrice, bedRoom, distance)
        url = self.baseUrl + self.rentBaseUrl + parameter
        yield scrapy.Request(url, headers=fakeHeader,meta = {'cookiejar' : 1})

    def parse(self, response):
        global fakeCookie
        global fakeHeader
        global currentPage
        open_in_browser(response)
        # inspect_response(response,self)

        # propertyTitle = response.css('ul.listing-items').xpath('li/div[1]/div[2]/h3/a/span/text()').extract()
        # propertyType = response.css('ul.listing-items').xpath('li/div[1]/div[2]/ul[1]/li/span/text()').extract()
        # propertyLocation = response.css('ul.listing-items').xpath('li/div[1]/div[2]/p/span/text()').extract()
        # propertySize = response.css('ul.listing-items').xpath('li/div[1]/div[2]/ul[2]/li[1]/text()').extract()
        # propertyFeature = response.css('ul.listing-items').xpath('li/div[1]/div[2]/ul[2]/li[1]/text()').extract()
        # propertyCost = response.css('ul.listing-items').xpath('li/div[1]/div[3]/div[1]/p/text()').extract()
        # propertyContactNumber = response.css('ul.listing-items').xpath('li/div[1]/div[3]/div[2]/a/span/text()').extract()
        # propertyContactPerson = response.css('ul.listing-items').css('div.listing-marketed').xpath('a/text()').extract()
        # propertyUpdateTime = response.css('ul.listing-items').css('div.listing-marketed').xpath('span/text()').extract()
        last_page = response.css('ul.pagination').xpath('li[position() = (last() - 1)]/a/text()').extract()
        last_page = int(last_page[0])
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
        if last_page and currentPage <= last_page:
            insertIndex = 0
            next_page = ''
            if currentPage == 1:
                insertIndex = response.url.index('?')
                currentPage += 1
                next_page = response.url[31:insertIndex] + '/{0}'.format(currentPage) + response.url[insertIndex:]
            else:
                insertIndex = response.url.index('/{0}'.format(currentPage))
                currentPage += 1
                next_page = response.url[31:insertIndex] + '/{0}'.format(currentPage) + response.url[insertIndex+2:]
            next_page = self.baseUrl + next_page
            yield scrapy.Request(next_page,headers=fakeHeader,callback=self.parse,meta = {'cookiejar' : 1})
