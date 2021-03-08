import scrapy

class uartlibSpider(scrapy.Spider):
    name = "uartlib"
    start_urls = [
        'http://uartlib.org'
    ]
    selectors = {
        'text': "//*[not(self::script)][not(self::style)]//text()[normalize-space()][not(contains(.,'{'))][not(contains(.,';'))]",
        'img': '//img/@src',
        'url': "//a/@href[starts-with(., '" + start_urls[0] + "')or starts-with(., '/')]"
    }
    def parse(self, response):
        texts = response.xpath(self.selectors['text']).extract()
        images = response.xpath(self.selectors['img']).extract()
        urls = response.xpath(self.selectors['url']).extract()
        yield {
            'url': response.url,
            'texts': texts,
            'images': images
        } 
        if response.url == self.start_urls[0]:
            links = [
                link for link in urls if link != "/"
            ]
            for link in links[:19]:
                if link.startswith("/"):
                    link = self.start_urls[0] + link
                yield response.follow(link, callback=self.parse)