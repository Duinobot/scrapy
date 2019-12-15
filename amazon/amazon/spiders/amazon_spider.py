# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonItem
from scrapy.utils.response import open_in_browser

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    start_urls = ['https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dstripbooks-intl-ship&field-keywords=']

    def parse(self, response):
        open_in_browser(response)
        items = AmazonItem()

        name = response.css("#dealTitle .a-declarative").extract()
        price = response.css('.a-price-fraction , .acs-product-block__price--buying .a-price-whole , .dealPriceText').css('::text').extract()
        imagelink = response.css("img::attr(src)").extract()
        review = response.css(".acs-product-block__rating__review-count").css('::text').extract()
        
        items["name"] = name
        items["price"] = price
        items["imagelink"] = imagelink
        items["review"] = review

        yield items["name"]