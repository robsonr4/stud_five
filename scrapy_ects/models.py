from functools import _make_key
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, User


class Titles(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "title"


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.ManyToManyField('Major', through='MajorStat')
    spec_stat = models.ManyToManyField('Specialization', through='SpecStat')
    major_course = models.ManyToManyField(
        'MajorCourse', through='MajorCourseStat')
    spec_course = models.ManyToManyField(
        'SpecCourse', through='SpecCourseStat')
    major_test = models.ManyToManyField('MajorTest', through='MajorCourseStat', blank=True, null=True)
    spec_test = models.ManyToManyField('SpecTest', through='SpecCourseStat', blank=True, null=True)
    major_assignment = models.ManyToManyField('MajorAssignment', through='MajorCourseStat', blank=True, null=True)
    spec_assignment = models.ManyToManyField('SpecAssignment', through='SpecCourseStat', blank=True, null=True)
    current_sem = models.IntegerField()
    album_nr = models.IntegerField()
    start_of_major = models.DateField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Major(models.Model):

    name = models.CharField(max_length=128)
    duration_in_sem = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Major(name="{self.name}", duration_in_sem={self.duration_in_sem}'

    class Meta:
        verbose_name = 'Major'
        verbose_name_plural = 'Majors'


class Specialization(models.Model):

    name = models.CharField(max_length=128)
    major = models.ForeignKey('Major', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'


class AbstractCourse(models.Model):

    ects = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

    class Meta:
        abstract = True
        verbose_name = 'AbstractCourse'
        verbose_name_plural = 'AbstractCourses'


class SpecCourseStat(AbstractCourse):

    spec_course = models.ForeignKey('SpecCourse', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    spec_test = models.ForeignKey(
        'SpecTest', on_delete=models.CASCADE, blank=True, null=True)
    spec_assignment = models.ForeignKey(
        'SpecAssignment', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.spec_course.name}'

    class Meta:
        verbose_name = 'SpecCourseStat'
        verbose_name_plural = 'SpecCourseStats'


class MajorCourseStat(AbstractCourse):

    major_course = models.ForeignKey('MajorCourse', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    major_test = models.ForeignKey(
        'MajorTest', on_delete=models.CASCADE)
    major_assignment = models.ForeignKey(
        'MajorAssignment', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.major_course.name}'

    class Meta:
        verbose_name = 'MajorCourseStat'
        verbose_name_plural = 'MajorCourseStats'


class MajorCourse(models.Model):
    name = models.CharField(max_length=128)
    major = models.ForeignKey('major', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class SpecCourse(models.Model):

    spec = models.ForeignKey('Specialization', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'SpecCourse'
        verbose_name_plural = 'SpecCourses'


class AbstractAssignment(models.Model):

    name = models.CharField(max_length=128)
    max_points = models.IntegerField()
    points = models.IntegerField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = 'AbstractAssignment'
        verbose_name_plural = 'AbstractAssignments'


class MajorAssignment(AbstractAssignment):

    class Meta:
        verbose_name = 'MajorAssignment'
        verbose_name_plural = 'MajorAssignments'


class SpecAssignment(AbstractAssignment):

    class Meta:
        verbose_name = 'SpecAssignment'
        verbose_name_plural = 'SpecAssignments'


class AbstractTest(models.Model):

    name = models.CharField(max_length=128)
    max_points = models.IntegerField()
    points = models.IntegerField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = 'AbstractTest'
        verbose_name_plural = 'AbstractTests'


class MajorTest(AbstractTest):

    class Meta:
        verbose_name = 'MajorTest'
        verbose_name_plural = 'MajorTests'


class SpecTest(AbstractTest):

    class Meta:
        verbose_name = 'SpecTest'
        verbose_name_plural = 'SpecTests'


class MajorStat(models.Model):

    major = models.ForeignKey('Major', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    max_ects = models.IntegerField(default=210)
    current_ects = models.IntegerField(default=sum)

    def __str__(self):
        return f'{self.student.user.first_name}: {self.major}'

    class Meta:
        verbose_name = 'MajorStat'
        verbose_name_plural = 'MajorStats'


class SpecStat(models.Model):

    spec = models.ForeignKey('Specialization', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student.user.first_name}: {self.spec}'

    class Meta:
        verbose_name = 'SpecStat'
        verbose_name_plural = 'SpecStats'
