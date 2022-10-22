import scrapy
from scrapy_playwright.page import PageMethod


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {
        'FEED_URI' : 'quotes.json',
        'FEED_FORMAT' : 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'USER_AGENT': 'DanielJoseMartinez',
    }

    def start_requests(self):
        url="http://quotes.toscrape.com/scroll"
        yield scrapy.Request(
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                errback=self.errback,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div.quote"),
                    PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    PageMethod("wait_for_selector", "div.quote:nth-child(11)"),  # 10 per page
                ],
            ),
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
            'text' : quote.xpath('./span[@class="text"]/text()').get(),
            'author': quote.xpath('./span/small[@class="author"]/text()').get(),
            'tags': quote.xpath('./div[@class="tags"]/a/text()').getall()
            }
            
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()