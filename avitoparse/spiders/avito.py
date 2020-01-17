# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva/kvartiry/prodam?cd=1']

    def parse(self, response: HtmlResponse):
        next_button = response.css('div.pagination-root-2oCjZ span.pagination-item-1WyVp.pagination-item_arrow-Sd9ID.pagination-item_readonly-2V7oG::attr(data-marker)').extract()
        if next_button != ['pagination-button/next']:
            active_page = response.css('div.pagination-root-2oCjZ span.pagination-item-1WyVp.pagination-item_active-25YwT::text').extract_first()
            next_page = 'https://www.avito.ru/moskva/kvartiry/prodam?cd=1' + '&p='+ str(int(active_page)+1)
            yield response.follow(next_page, callback= self.parse)
        offers = response.css('div.js-catalog_serp div.snippet-horizontal.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended div.item__line div.item_table-wrapper a.snippet-link::attr(href)').extract()
        for offer in offers:
            offer = 'https://www.avito.ru'+offer
            yield response.follow(offer, callback=self.offer_parse)
        pass
    
    def offer_parse(self, response: HtmlResponse):
        title = response.css('div.item-view-content div.title-info-main h1.title-info-title span.title-info-title-text::text').extract_first()
        price = response.css('div.item-view-content div.item-price-wrapper span.js-item-price::attr(content)').extract_first()
        parameter_keys = response.css('div.item-view-block ul.item-params-list li.item-params-list-item span.item-params-label::text').extract()
        parameter_values = response.css('div.item-view-block ul.item-params-list li::text').extract()
        parameters = {}
        for key in parameter_keys:
            parameters[key] = parameter_values[2 * parameter_keys.index(key) + 1]

        yield {'title': title, 'price': price, 'parameters':parameters}
        pass
