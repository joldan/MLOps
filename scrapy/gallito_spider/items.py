# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class GallitoSpiderItem(scrapy.Item):
	# Metadata
	id = Field()
	date = Field()
	url = Field()
	# Posting information
	building_type = Field()
	deal_type = Field()
	location = Field()
	rooms = Field()
	bathrooms = Field()
	area = Field()
	price = Field()
	title = Field()
	# Image info
	image_urls = Field()
	images = Field()


