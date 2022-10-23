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
        yield scrapy.Request(
            url="http://quotes.toscrape.com/scroll",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                errback=self.errback,
                playwright_page_methods=[
                    PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod('wait_for_selector', f'.quote:nth-child(11)'),
                    PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod('wait_for_selector', f'.quote:nth-child(21)'),
                    PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod('wait_for_selector', f'.quote:nth-child(31)'),
                    PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod('wait_for_selector', f'.quote:nth-child(41)'),
                    PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod('wait_for_selector', f'.quote:nth-child(51)'),
                    PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod('wait_for_selector', f'.quote:nth-child(61)'),
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