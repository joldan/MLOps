# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import scrapy 
from PIL import Image
from scrapy.pipelines.images import ImagesPipeline

class customImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, item=None):
    # Customize the filename based on your requirements
        filename = item['id']
        #ptin
        #filename = request.url.split('/')[-1]
        return filename

#    def item_completed(self, results, item, info):
#        for result, image_info in results:
#            if result:
#                path = image_info['path']
#                img = Image.open(path)
                # here is where you do your resizing - this method overwrites the
                # original image you will need to create a copy if you want to keep
                # the original.
#                img = img.resize((256, 256))
#                img.save(path)
#        return item