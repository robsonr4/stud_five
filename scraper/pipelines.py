# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import django


class DjangoPipeline:
    def process_item(self, item, spider):
        # try:
        #     item.save()
        #     return item
        # except django.db.utils.IntegrityError:
        #     pass
        item.save()
        return item

# def process_item(self, item, spider):
#         for itemik in item:
#             itemik.save()
#         return item   