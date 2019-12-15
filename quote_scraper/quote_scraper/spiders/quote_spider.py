import scrapy
from ..items import QuoteScraperItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

 
class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/login'
    ]

    def parse(self, response):
        token = response.css("input[name='csrf_token']::attr(value)").extract_first()
        return FormRequest.from_response(response,formdata = 
            {"csrf_token": token,
            "username": "jb",
            "password": "j8"},
            callback = self.start_scraping)

    def start_scraping(self, response):
        open_in_browser(response)
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