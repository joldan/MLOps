__author__ = "LaLOSS"

from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import datetime
import re


# Get the current date and time
current_datetime = datetime.datetime.now()

# Print the current date and time
print(current_datetime)

class MyscrapyItem(Item):
	building_type = Field()
	deal_type = Field()
	location = Field()
	rooms = Field()
	bathrooms = Field()
	area = Field()

	price = Field()
	title = Field()
	
	url = Field()
	date = Field()

class gallitoCrawler(CrawlSpider):
	name = "gallito_crawler"
	start_urls = ["https://www.gallito.com.uy/inmuebles/apartamentos"]
	allowed_domains = ['gallito.com.uy']
	
	custom_settings = {
		"USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ),
		"max_items_per_label": 2,
        "label_field": "property_type",
        "CLOSESPIDER_ITEMCOUNT": 5,
    }

	rules = {
		Rule(LinkExtractor(allow=r'\/inmuebles\/apartamentos\?pag=\d+')),
		Rule(LinkExtractor(allow=(r"-\d{8}$")), callback="parse"),
	}

	def parse(self, response):
		item = MyscrapyItem()
		item['price'] = response.xpath('/html/body/form/main/div/section/div/div[2]/span/text()').get()
		item['title'] = response.xpath('/html/body/form/main/div/section/div/h1/text()').get()
		
		res = response.css('#div_datosOperacion .wrapperDatos')	
		attribute_classes = {'fas fa-building':'building_type', 'fas fa-handshake':'deal_type', 'fas fa-map-marked':'location', 'fas fa-bed':'rooms', 'fas fa-bath':'bathrooms', 'far fa-square':'area'}	
		print(len(res.getall(ß)))
		for child in res:
			p_value = child.css('div.wrapperDatos > p::text').get()
			i_class = child.css('div.wrapperDatos > div.iconoDatos > i::attr(class)').get()
			item[attribute_classes[i_class]] = p_value

			# Select all elements with class 'wrapperDatos' within the element with id 'div_datosOperacion'
			res = response.css('#div_datosOperacion .wrapperDatos')
			# Define a dictionary mapping icon classes to item attributes
			attribute_classes = {'fas fa-building': 'building_type', 'fas fa-handshake': 'deal_type', 'fas fa-map-marked': 'location',
                     			'fas fa-bed': 'rooms', 'fas fa-bath': 'bathrooms', 'far fa-square': 'area'}
			# Iterate over each element in the list "res"
			for index, child in enumerate(res):
				# Get the text value of the <p> element within the child element
				p_value = child.css('div.wrapperDatos > p::text').get()
				# Get the class attribute of the <i> element within the child element
				i_class = child.css('div.wrapperDatos > div.iconoDatos > i::attr(class)').get()
				# Map the icon class to the corresponding attribute name and assign the value to correct 'item' attribute
				# In case of ammount of bathrooms and rooms use regex to just keep the number amount
				if(i_class == "fas fa-bed" or i_class == "fas fa-bath"):
					try:
						item[attribute_classes[i_class]] = re.findall(r'\d+', p_value).pop()
						break
					except Exception:
						item[attribute_classes[i_class]] = 0 
				else:
					item[attribute_classes[i_class]] = p_value





		item['date'] = datetime.datetime.now()
		item['url'] = response.url
		return item 

	def parse_atributes(response):
		attributes = response.xpath('//*[@id="div_datosOperacion"]').get()
		return attributes

