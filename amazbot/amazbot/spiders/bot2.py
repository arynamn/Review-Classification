# -*- coding: utf-8 -*-
import scrapy


class Bot2Spider(scrapy.Spider):
    name = 'bot2'
    allowed_domains = ['www.amazon.in']
    start_urls = [
        'https://www.amazon.in/Kraft-Seeds-African-Marigold-Multicolour/product-reviews/B07G878PQZ/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
    ]

    def parse(self, response):
        rev = response.css('.review-text-content span::text').extract()
        for item in rev:
            yield{
                'Review' : item
            }
        
        links = response.css('li.a-last a::attr(href)').extract()
        for link in links:
            next = response.urljoin(link)
            yield response.follow(url = next , callback = self.parse)