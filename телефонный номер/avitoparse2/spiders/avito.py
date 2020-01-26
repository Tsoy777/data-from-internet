# -*- coding: utf-8 -*-
# Ресурс: avito.ru/
#
import scrapy
from scrapy.http import HtmlResponse
from avitoparse2.items import AvitoparseItem

HASHES = {
    'phone':'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir',
}

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['m.avito.ru']
    start_urls = ['https://m.avito.ru/moskva/kvartiry/prodam']
    start_urls_old=['https://www.avito.ru/moskva/kvartiry/prodam?cd=1']

    def parse(self, response: HtmlResponse):
        for i in range(2,10):
            next_page = f'/api/9/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=637640&categoryId=24&page={i}&lastStamp=1580022600&display=list&limit=30'
            yield response.follow(next_page, callback=self.parse)
        url_offers = response.xpath('//div[contains(@data-marker,"items/list")]//div[contains(@data-marker,"item/title")]//a/@href').extract()

        for url_offer in url_offers:
            offer_id = url_offer[-10:]
            yield response.follow(
                url_offer,
                callback=self.data_parse,
                cb_kwargs={'offer_id': offer_id},
            )
        pass

    def data_parse(self, response: HtmlResponse, offer_id):
        item = AvitoparseItem(
            url=response.url,
            title=response.xpath('//h1[contains(@data-marker,"item-description/title")]/span/text()').extract_first(),
            price=response.xpath('//span[contains(@data-marker,"item-description/price")]/text()').extract_first(),
            parameters=response.xpath('//div[contains(@data-marker,"item-properties/list")]/div/div/div/text()').extract(),
        )
        url = f"/api/1/items/{offer_id}/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"
        yield response.follow(
            url,
            callback=self.get_phone,
            cb_kwargs={'item': item},
        )
        pass

    def get_phone(self, response:HtmlResponse, item: AvitoparseItem):
        number = response.text.split('=%')[-1][2:-4]
        item['phone_number'] = number
        yield item
        pass

#----------------------------------------------------------------------------------Старый парсер

    def old_parse(self, response:HtmlResponse):
        next_button = response.css('div.pagination-root-2oCjZ span.pagination-item-1WyVp.pagination-item_arrow-Sd9ID.pagination-item_readonly-2V7oG::attr(data-marker)').extract()
        if next_button != ['pagination-button/next']:
            active_page = response.css('div.pagination-root-2oCjZ span.pagination-item-1WyVp.pagination-item_active-25YwT::text').extract_first()
            next_page = 'https://www.avito.ru/moskva/kvartiry/prodam?cd=1' + '&p='+ str(int(active_page)+1)
            yield response.follow(next_page, callback= self.parse)
        offers = response.css('div.js-catalog_serp div.snippet-horizontal.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended div.item__line div.item_table-wrapper a.snippet-link::attr(href)').extract()
        for offer in offers:
            offer = 'https://www.avito.ru'+offer
            yield response.follow(offer, callback=self.offer_parse)

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
