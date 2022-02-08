import scrapy
from scraper.items import MajorCourseItem, MajorCourseStatItem, MajorItem, StudentItem, MajorStatItem
from django.contrib.auth.models import User
from scrapy_ects.models import Major, MajorCourse, MajorStat, Student
from django.db.models import Q


class EctsSpider(scrapy.Spider):
    name = 'ects'
    start_urls = ['https://cas.swps.edu.pl/cas/login', ]
    """Scrapes sites
       -------------
    https://portal.swps.edu.pl/pl/group/common/profile ,
    https://portal.swps.edu.pl/pl/group/common/profile .

    Yields objects
    --------------
    Major,
    Student,
    MajorStat
    MajorCourse,
    MajorCourseStat.

    To be updated/corrected
    -----------------------
    # request.user,
    Shorten functions since there is repeating in crawled sites,
    Yield specs in the future.
    """

    def parse(self, response):
        """Logs into SWPS.
        Calls after_login func.
        """

        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'rfalkowski@st.swps.edu.pl',  # request.user
                      'password': 'Sepuku44!'},  # request.user
            callback=self.after_login
        )

    def after_login(self, response):
        """Navigates to main screen. 
        Calls major_part func.
        """

        scrapy.Request(
            url="https://portal.swps.edu.pl/pl/group/student/home?swps_redirect_target=true", dont_filter=True)
        return scrapy.Request(url="https://portal.swps.edu.pl/pl/group/common/profile", dont_filter=True, callback=self.profile)

    def profile(self, response):
        """Site: https://portal.swps.edu.pl/pl/group/common/profile .

        Scrapes Major's attribute name. 
        Calls major_item_finito func with scraped name as kwargs.
        """

        przebieg = response.xpath(
            "//div[@class='col-xs-8 pl0']/text()").getall()

        # Update User.email
        b = User.objects.get(username='falko')  # request.user
        b.email = response.xpath("//div[@class='ramka p15']/a/text()").get()
        b.save()

        return scrapy.Request(
            "https://zapisy.swps.edu.pl/study-program",
            dont_filter=True,
            callback=self.major_item_finito,
            cb_kwargs={
                'name': przebieg[2],
                'album_nr': przebieg[0]
            }
        )

    def major_item_finito(self, response, name, album_nr):
        """Site: https://zapisy.swps.edu.pl/study-program .

        Scrapes Major's duration. 
        Yields MajorItem. 
        Calls student func with scraped duration as kwargs.
        """

        # Yield MajorItem
        major_item = MajorItem()

        # Major.name
        major_item['name'] = name

        # Major.duration_in_sem
        dur_sem = response.xpath("//div[@class='progsem']/text()").getall()[-1]
        dur_sem = dur_sem.removeprefix(
            '\n    \t\t\t\t\t\tSEM ').removesuffix('\n    \t\t\t\t\t')
        major_item['duration_in_sem'] = int(dur_sem)

        yield major_item

        yield scrapy.Request(
            url="https://portal.swps.edu.pl/pl/group/common/profile",
            dont_filter=True,
            callback=self.student,
            cb_kwargs={'dur_sem': dur_sem}
        )

    def student(self, response, dur_sem):
        """Site: https://portal.swps.edu.pl/pl/group/common/profile .

        Scrapes Student's album_nr. 
        Yields StudentItem.
        Scrapes User's email.
        Updates User.
        Scrapes MajorStat's department.
        Yields MajorStatItem.
        Calls program func.
        """

        przebieg = response.xpath(
            "//div[@class='col-xs-8 pl0']/text()").getall()

        # Yield StudentItem
        student_item = StudentItem()
        # Student.album_nr
        student_item['album_nr'] = int(przebieg[0])

        # Student.user
        student_item['user'] = User.objects.get(
            username='falko')  # request.user

        yield student_item

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

        yield scrapy.Request(
            url="https://zapisy.swps.edu.pl/study-program",
            dont_filter=True,
            callback=self.program,
        )

    def program(self, response):
        """Site: https://zapisy.swps.edu.pl/study-program .

        Scrapes MajorCourse's: name, major.
        Yields MajorCourseItem.
        Scrapes MajorCourseStat's: major_course, degree, ects, student, course_passed.
        Yields MajorCourseStatItem.

        MajorCourseStatItem:
        Semester attribute,
        Lecturer attribute,
        Sylabus attribute,
        Total points scored attribute.
        """

        long_courses_path = response.xpath(
            "//td[@class='progwewtd2']").getall()

        sem_path = response.xpath("//table[@class='zapisy']/text()").getall()

        # Yield MajorCourseStatItem
        for i in range(len(long_courses_path)):
            course_item = MajorCourseItem()

            # MajorCourse.name
            course_name_later = response.xpath(
                "//td[@class='progwewtd2']/text()").getall()[i]
            course_item['name'] = course_name_later.strip()

            # MajorCourse.major
            course_attended = Student.objects.get(
                user__username='falko').major.get()  # request.user
            course_item['major'] = course_attended

            yield course_item

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        # Yield MajorCourseStatItem
        for h, sem in enumerate(sem_path):
            try:
                short_courses_path = response.xpath(
                    f"//table[@class='zapisy'][{h+1}]//tr[@class='prog']").getall()
                for i, course_name in enumerate(short_courses_path):
                    long_in_short_path = response.xpath(f"//table[@class='zapisy'][{h+1}]//tr[@class='prog'][{i+1}]//table[@class='progwew']").getall()
                    for j, right_name in enumerate(long_in_short_path):
                        course_stat_item = MajorCourseStatItem()

                        # MajorCourseStat.major_course
                        course_stat_item['major_course'] = MajorCourse.objects.get(
                            name=response.xpath(f"//table[@class='zapisy'][{h+1}]//tr[@class='prog'][{i+1}]//table[@class='progwew'][{j+1}]//td[@class='progwewtd2']/text()").get().strip())

                        # MajorCourseStat.degree
                        ocena = response.xpath(
                            f"//table[@class='zapisy'][{h+1}]//tr[@class='prog'][{i+1}]//table[@class='progwew'][{j+1}]//span[@class='progocena']/text()").get().strip()
                        if ocena != '' and ocena != 'Zal':
                            course_stat_item['degree'] = float(ocena.strip())
                        elif ocena == 'Zal' or ocena == '':
                            course_stat_item['degree'] = 0

                        # MajorCourseStat.ects
                        if response.xpath(
                                f"//table[@class='zapisy'][{h+1}]//tr[@class='prog'][{i+1}]//td[@class='c4']/text()").get().strip().removesuffix(' ECTS') != '':
                            ect = int(response.xpath(
                                f"//table[@class='zapisy'][{h+1}]//tr[@class='prog'][{i+1}]//td[@class='c4']/text()").get().strip().removesuffix(' ECTS'))
                            if len(long_in_short_path) > 1:
                                ect /= len(response.xpath(
                                    f"//table[@class='zapisy'][{h+1}]//tr[@class='prog'][{i+1}]//td[@class='progwewtd2']/text()").getall())
                        else:
                            ect = 0
                        course_stat_item['ects'] = ect

                        # MajorCourseStat.student
                        course_stat_item['student'] = Student.objects.get(
                            user__username='falko')

                        # MajorCourseStat.course_passed
                        passed = ocena != '' or ocena == 'Zal'
                        course_stat_item['course_passed'] = True if passed else False

                        # MajorCourseStat.semester
                        course_stat_item['semester'] = int(response.xpath(f"//div[@class='progsem'][{h+1}]/text()").get().strip().removeprefix('SEM '))

                        # MajorCourseStat.lecturer
                        course_stat_item['lecturer'] = response.xpath(
                            f"//table[@class='zapisy'][{h+1}]//tr[@class='prog'][{i+1}]//table[@class='progwew'][{j+1}]//a[@class='tooltipped']/@data-tooltip").get()

                        # MajorCourseStat.sylabus

                        yield course_stat_item
            except IndexError:
                continue
