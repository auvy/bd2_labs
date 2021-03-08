import scrapy

class hozmartSpider(scrapy.Spider):
    name = "hozmart"
    start_urls = [
        'https://hozmart.com.ua/uk/15-benzopili',
        'https://hozmart.com.ua/uk/15-benzopili?p=2'
    ]
    selectors = {
        'all_items': "//ul[contains(@id, 'product_list')]/li",
        'names': ".//a[contains(@class, 'b1c-name-uk')]/text()",
        'images': ".//img[contains(@class, 'b1c-img')]/@src",
        'prices': ".//span[contains(@class, 'price')]/text()",
        'available': ".//p[contains(@class, 'availability')]/span//text()[normalize-space()]"
    }
    def parse(self, response):
        for result in response.xpath(self.selectors['all_items'])[:20]:
            yield {
                'names': result.xpath(self.selectors['names']).extract_first(),
                'images': result.xpath(self.selectors['images']).extract_first(),
                'prices': result.xpath(self.selectors['prices']).extract_first(),
                'avails': result.xpath(self.selectors['available']).extract_first().strip()
            } 