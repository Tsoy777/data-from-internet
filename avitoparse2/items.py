# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AvitoparseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
#Заголовок
# URL
# Предлагаемая ЗП
# Список ключевых навыков
# Название организации разместившей вакансию
# Ссылка на страницу организации разместившей организацию
# Ссылку на логотип организации
class HhItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    skills = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    company_logo = scrapy.Field()
