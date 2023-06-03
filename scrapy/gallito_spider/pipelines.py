# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import scrapy 
from scrapy.pipelines.images import ImagesPipeline

class customImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, item=None):
    # Customize the filename based on your requirements
        filename = item['id']
        #ptin
        #filename = request.url.split('/')[-1]
        return filename

