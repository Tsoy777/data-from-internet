from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from avitoparse import settings
from avitoparse.spiders.avito import AvitoSpider
from avitoparse.spiders.hh import HhSpider

if __name__=='__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings= scr_settings)
   # process.crawl(AvitoSpider)
    process.crawl(HhSpider)
    process.start()
