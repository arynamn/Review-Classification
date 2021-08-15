# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import FlipbotItem

class Bot1Spider(scrapy.Spider):
    name = 'bot1'
    allowed_domains = [
       'www.flipkart.com'
       ]
    start_urls = [
        'https://www.flipkart.com/huggies-wonder-pants-diaper-l/product-reviews/itm632e0488dc7db?pid=DPRFCMVBBYQKTVYZ'
        ]
    def parse(self, response):
        rev = response.css('.qwjRop div::text').extract()
        for item in rev:
            yield{
                'Review' : item
            }

        links = response.css('._3fVaIS ::attr(href)').extract()
        curr_temp = response.request.url.split('page')
        if len(curr_temp) == 1:
                curr_num = 1
        else:
            curr_nums = re.findall('\d+',curr_temp[1])
            curr_num = curr_nums[0]

        for link in links:
            next = response.urljoin(link)
            next_temp = next.split('page')
            next_nums = re.findall('\d+',next_temp[1])
            next_num = next_nums[0]
            if int(next_num) > int(curr_num):
                yield{
                    'Review' : next_num
                }                      
                yield response.follow(url = next, callback = self.parse)