import os
from scrapy import cmdline
from lxml import etree

mainpath = os.path.dirname(__file__) + '/lab1'
root = None

def task_1_parse():
    cmdline.execute("scrapy crawl uartlib".split())

def task_1_processing():
    result = open(mainpath + '/results/o_uartlib.xml', 'rb')
    root = etree.parse(result)
    result.close()

    pageCount = root.xpath('count(//page)')
    textCount = root.xpath('count(//fragment[@type="text"])')
    result = 'Average count of text fragments per page: %f' % (textCount / pageCount)

    f = open(mainpath + '/results/r_uartlib.txt', 'w')
    f.write(result)
    f.close()


def task_2_parse():
    cmdline.execute("scrapy crawl hozmart".split())

def task_2_processing():
    dom = etree.parse(mainpath + '/results/o_hozmart.xml')
    xslt = etree.parse(mainpath + '/hozmart.xslt')
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    with open(mainpath + '/results/r_hozmart.html', 'wb') as f:
        f.write(etree.tostring(newdom, pretty_print=True))


task_1_parse()

