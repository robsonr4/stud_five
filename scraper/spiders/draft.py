import scrapy
from scraper.items import MajorCourseItem, MajorCourseStatItem, MajorItem, StudentItem, MajorStatItem
from django.contrib.auth.models import User
from scrapy_ects.models import Major, MajorCourse, MajorStat, Student
from django.db.models import Q

def profile(self, response):

    przebieg = response.xpath(
            "//div[@class='col-xs-8 pl0']/text()").getall()
    # Update User.email
    b = User.objects.get(username='falko')  # request.user
    b.email = response.xpath("//div[@class='ramka p15']/a/text()").get()
    b.save()

    # Yield StudentItem
    student_item = StudentItem()

    # Student.album_nr
    student_item['album_nr'] = int(przebieg[0])

    # Student.user
    student_item['user'] = User.objects.get(
            username='falko') 

    yield scrapy.Request(
            url="https://portal.swps.edu.pl/pl/group/common/profile",
            dont_filter=True,
            callback=self.student,
            cb_kwargs={'dur_sem': dur_sem}
        )
  

    if MajorStat.objects.filter(Q(major=Major.objects.get(name=przebieg[2], duration_in_sem=dur_sem)) & Q(student=Student.objects.get())).exists() == False:
            # Yield MajorStatItem
            major_stat_item = MajorStatItem()

            # MajorStat.major
            major_stat_item['major'] = Major.objects.get(
                name=przebieg[2], duration_in_sem=dur_sem)

            # MajorStat.student
            major_stat_item['student'] = Student.objects.get(
                user__username='falko')  # request.user

            # MajorStat.department
            major_stat_item['department'] = przebieg[1]

            yield major_stat_item