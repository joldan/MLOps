# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class GallitoSpiderItem(scrapy.Item):
	tipo = Field()
	baños = Field()
	dormitorios = Field()
	precio = Field()
	titulo = Field()
