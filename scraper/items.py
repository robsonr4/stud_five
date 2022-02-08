# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from scrapy_ects.models import Major, MajorCourse, MajorCourseStat, MajorStat, Student


class MajorCourseStatItem(DjangoItem):
    django_model = MajorCourseStat


class MajorStatItem(DjangoItem):
    django_model = MajorStat


class StudentItem(DjangoItem):
    django_model = Student


class MajorItem(DjangoItem):
    django_model = Major


class MajorCourseItem(DjangoItem):
    django_model = MajorCourse
