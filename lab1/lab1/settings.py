BOT_NAME = 'lab1'

SPIDER_MODULES = ['lab1.spiders']
NEWSPIDER_MODULE = 'lab1.spiders'

ITEM_PIPELINES = {'lab1.pipelines.lab1Pipeline': 100}

ROBOTSTXT_OBEY = False
