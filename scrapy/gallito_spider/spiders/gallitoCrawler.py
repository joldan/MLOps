__author__ = "LaLOSS"

from scrapy import signals
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from gallito_spider.items import GallitoSpiderItem
import datetime
import re
from gallito_spider.azure_helpers import upload_metadata_file, upload_images

class gallitoCrawler(CrawlSpider):
	name = "gallito_crawler" 
	id = 0 # ID to track relation between metadata line and image

	custom_settings = {
		"USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ),
		"max_items_per_label": 2,
        "label_field": "property_type",
        "CLOSESPIDER_ITEMCOUNT": 50000,  # Modifiy this values to change the max pages scraped
    }

	start_urls = ["https://www.gallito.com.uy/inmuebles/apartamentos/venta","https://www.gallito.com.uy/inmuebles/casas/venta"]
	#start_urls = ["https://www.gallito.com.uy/inmuebles/apartamentos","https://www.gallito.com.uy/inmuebles/casas"]
	allowed_domains = ['gallito.com.uy']

	rules = {
		Rule(LinkExtractor(allow=[r'\/inmuebles\/apartamentos\/venta\?pag=\d+',r'\/inmuebles\/casas\/venta\?pag=\d+'])),
		Rule(LinkExtractor(allow=(r"-\d{8}$")), callback="parse"),
	}

	def parse(self, response):
		item = GallitoSpiderItem()
		## scrape tabular data
		item['price'] = response.xpath('/html/body/form/main/div/section/div/div[2]/span/text()').get()
		item['title'] = response.xpath('/html/body/form/main/div/section/div/h1/text()').get()

		item['department'] = response.xpath('/html/body/form/nav/ol/li[5]/a/text()').get()
		## scrape tabular data inside the wrapperDatos section in the page. 
		res = response.css('#div_datosOperacion .wrapperDatos')	
		attribute_classes = {'fas fa-building':'building_type', 'fas fa-handshake':'deal_type', 'fas fa-map-marked':'location', 'fas fa-bed':'rooms', 'fas fa-bath':'bathrooms', 'far fa-square':'area'}	
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
		## scrape image URL, only the first image is used
		item['image_urls'] = response.css('#galeria img::attr(src)').extract()[:1] #Se toma 

		#ID is created
		item['id'] = self.id
		self.id += 1
		
		pattern = r"(?<=-)\d+"
		item['foreign_id'] = re.findall(pattern, response.url)[-1]

		# Date and URL 
		item['date'] = datetime.datetime.now()
		item['url'] = response.url
		return item 

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(gallitoCrawler, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		today = datetime.date.today().isoformat()
		spider.logger.info("Spider closed: %s", "UPLOADING FILES TO FOLDER ")
		#upload_metadata_file()
		#upload_images()