from scrapy.spiders import CrawlSpider
from scrapy.http import FormRequest

from ..items import QuotetutorialItem


class QuoteSpider(CrawlSpider):

    name = 'quote'
    start_urls = [
        'http://quotes.toscrape.com/login'
    ]

    def parse(self, response):

        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response, formdata={
                'csrf_token': token,
                'username': 'hammad',
                'password': 'rauf'
        }, callback=self.product)

    def product(self, response):

        product = QuotetutorialItem()

        fields = response.css('.quote')

        for field in fields:

            product['title'] = field.css('span.text::text').extract()
            product['author'] = field.css('.author::text').extract()
            product['tags'] = field.css('a.tag::text').extract()

            yield product

        next_page = response.css('.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback= self.product)