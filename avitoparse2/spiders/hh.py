# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avitoparse.items import HhItem

class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = [f'https://hh.ru/search/vacancy?area=1&clusters=true&enable_snippets=true&no_magic=true&text=it+%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA&from=SIMILAR_QUERY&page={page}' for page in range(0,73)]

    def parse(self, response: HtmlResponse):
        for url in response.xpath('//div[@class="resume-search-item__name"]/span[@class="g-user-content"]/a/@href').extract():
            yield response.follow(url, callback=self.adv_parse)
        pass


    def adv_parse(self, response: HtmlResponse):
        item = HhItem(
        url = response.url,
        title = response.xpath('//div[@class="vacancy-title"]/h1/span/text()').extract_first(),
        salary = response.xpath('//div[@class="vacancy-title"]/p/text()').extract(),
        skills = response.xpath('//div[@class="bloko-tag-list"]/div/div[@class="bloko-tag bloko-tag_inline"]/span/text()').extract(),
        company_name = response.xpath('//div[@class="vacancy-company-name-wrapper"]/a[@class="vacancy-company-name"]/span/span/text()').extract_first(),
        company_url = response.xpath('//div[@class="vacancy-company-name-wrapper"]/a[@class="vacancy-company-name"]/@href').extract_first(),
        company_logo = response.xpath('//a[@class="vacancy-company-logo"]/img/@src').extract_first(),
        )
        if item['title'] == None:
            item['title'] = response.xpath('//div[@class="vacancy-title "]/h1/text()').extract_first()
            item['salary'] = response.xpath('//p[@class="vacancy-salary"]/text()').extract()
            item['skills'] = response.xpath('//span[contains(@data-qa,"skills-element")]/span/@title').extract()
            item['company_name'] = response.xpath('//p[@class="vacancy-company-name-wrapper"]/a[@class="vacancy-company-name"]/span/text()').extract_first()
            item['company_url'] = response.xpath('//p[@class="vacancy-company-name-wrapper"]/a[@class="vacancy-company-name"]/@href').extract_first()
            item['company_logo'] = response.xpath('//a[@class="vacancy-company-logo "]/img/@src').extract_first()
        yield item
        pass
