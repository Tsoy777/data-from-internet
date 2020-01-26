from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from avitoparse2 import settings
from avitoparse2.spiders.avito import AvitoSpider
from avitoparse2.spiders.hh import HhSpider

if __name__=='__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings= scr_settings)
    process.crawl(AvitoSpider)
    #process.crawl(HhSpider)
    process.start()
