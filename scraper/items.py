# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from scrapy_ects.models import Titles

class TitlesItem(DjangoItem):
    django_model = Titles
