import scrapy
from ..items import QuoteScraperItem


 
class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):

        items = QuoteScraperItem()

        all_div_quotes = response.css('div.quote')

        for quote in all_div_quotes:
            title = quote.css('span.text:first-child::text').extract()
            author = quote.css('small.author::text').extract()
            tags = quote.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            yield items
        
        next_page = response.css('li.next a[href]::attr(href)').get()

        if next_page is not None:
            print(next_page)
            yield response.follow(next_page, callback=self.parse)