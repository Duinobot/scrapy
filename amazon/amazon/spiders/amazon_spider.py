# -*- coding: utf-8 -*-
# follow this link
# https://www.youtube.com/playlist?list=PLhTjy8cBISEqkN-5Ku_kXG4QW33sxQo0t

import scrapy
from ..items import AmazonItem
from scrapy.utils.response import open_in_browser

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    start_urls = ['https://www.amazon.com/s?k=product&i=stripbooks-intl-ship&page=1&qid=1576464253&ref=sr_pg_2']
    page_number = 2

    def parse(self, response):
        
        item = AmazonItem()
        books = response.css('.s-include-content-margin')
        
        for book in books:
            name = book.css(".a-color-base.a-text-normal").css('::text').extract()
            price = book.css('.a-spacing-top-small .a-price span span').css('::text').extract()
            imagelink = book.css(".s-image::attr(src)").extract()
            review = book.css(".a-size-small .a-size-base").css('::text').extract()
            item['name'] = name
            item['price'] = price
            item['imagelink'] = imagelink
            item['review'] = review
            yield item
        
        next_page = "https://www.amazon.com/s?k=product&i=stripbooks-intl-ship&page="+ str(AmazonSpiderSpider.page_number) +"&qid=1576464253&ref=sr_pg_2"
        
        if AmazonSpiderSpider.page_number <= 75:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)