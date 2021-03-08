from lxml import etree
import os

class lab1Pipeline(object):
    def open_spider(self, spider):
        self.root = etree.Element("data")

    def close_spider(self, spider):
        f = open(os.path.dirname(__file__) + '/results/o_' + spider.name + '.xml', 'wb')
        f.write(etree.tostring(
            self.root, encoding="UTF-8",
            pretty_print=True
        ))
        f.close()

    def process_item(self, item, spider):
        if spider.name == "uartlib":
            page = etree.SubElement(self.root, "page", url=item["url"])
            for text in item['texts']:
                etree.SubElement(page, 'fragment', type='text').text = text
            for url in item['images']:
                etree.SubElement(page, 'fragment', type='image').text = url
            self.root.append(page)
        else:
            product: etree.Element = etree.Element("product")
            
            name = etree.Element("name")
            name.text = item["names"]

            price = etree.Element("price")
            price.text = item["prices"]

            image = etree.Element("image")
            image.text = item["images"]

            avail = etree.Element("availability")
            avail.text = item["avails"]

            product.append(name)
            product.append(price)
            product.append(image)
            product.append(avail)

            self.root.append(product)
        return item
