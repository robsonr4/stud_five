from typing import ValuesView
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Student, MajorCourseStat, MajorAssignment, MajorTest, SpecAssignment, SpecTest
from django.db.models import Q
# Create your views here.

def labels_getter():
    labels_obj = MajorCourseStat.objects.filter(semester=3).order_by("major_course__name")
    labels = []
    for label in labels_obj:
        labels.append(label.major_course.name)
    return labels

def points_getter():
    labels = labels_getter()
    point_obj = MajorAssignment.objects.filter(course_stat__major_course__name__in = labels).order_by("course_stat__major_course__name")
    points = []
    for label in labels:
        points_sum = 0

        for point in point_obj:
            if point.course_stat.major_course.name == label:
                points_sum += point.points

        points.append(points_sum)
    return points

def assignments_and_test():
    labels = labels_getter()
    m_assign_obj = MajorAssignment.objects.filter(course_stat__major_course__name__in = labels).order_by("course_stat__major_course__name")
    m_test_obj = MajorTest.objects.filter(course_stat__major_course__name__in = labels).order_by("course_stat__major_course__name")
    s_assign_obj = SpecAssignment.objects.filter(course_stat__spec_course__name__in = labels).order_by("course_stat__spec_course__name")
    s_test_obj = SpecTest.objects.filter(course_stat__spec_course__name__in = labels).order_by("course_stat__spec_course__name")

    lista = []
    lista.extend(m_assign_obj)
    lista.extend(m_test_obj)
    lista.extend(s_assign_obj)
    lista.extend(s_test_obj)

    names = set()

    for name in lista:
        try:
            names.add(name.course_stat.major_course.name)
        except AttributeError:
            names.add(name.course_stat.spec_course.name)
    
    loop = {name: [] for name in names}
    for name in names:
        print("1. ", name)
        for row in lista:
            try:
                i = row.course_stat.major_course.name
            except AttributeError:
                i = row.course_stat.spec_course.name
            print("2. ", i)
            if i == name:
                loop[name].append(row)
    
    yield loop
    yield names

class MainView(View):
    def get(self, request, *args, **kwargs):
        
        dates = MajorAssignment.objects.filter(Q(has_date=True)).order_by('the_date')
        
        return render(request, 'home.html', {
            "labels": labels_getter(),
            "datas": points_getter(),
            "closest_date": dates[0],
            "dates": dates[1:]
            })

class UniView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'uni.html', {})

class UniPointsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "uni_points.html", {
            "labels": labels_getter(),
            "datas": points_getter()
        })

class UniTestView(View):
    def get(self, request, *args, **kwargs):

        sth = assignments_and_test()

        return render(request, "uni_test.html", {
            "atest": next(sth),
            "names": next(sth)
        })

class UniInfoView(View):
    def get(self, request, *args, **kwargs):
        stud = Student.objects.get(user = request.user)
        major = stud.major.through.objects.get().major.name
        return render(request, "uni_info.html", {
            "us":stud,
            "major": major
        })