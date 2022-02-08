from django.contrib import admin
from scrapy_ects.models import Student, Major, Spec, MajorCourse, SpecCourse, MajorAssignment, SpecAssignment, MajorTest, SpecTest, MajorStat, MajorCourseStat, SpecCourseStat, SpecStat
# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    pass


class MajorAdmin(admin.ModelAdmin):
    pass


class SpecAdmin(admin.ModelAdmin):
    pass


class MajorCourseAdmin(admin.ModelAdmin):
    pass


class SpecCourseAdmin(admin.ModelAdmin):
    pass


class MajorAssignmentAdmin(admin.ModelAdmin):
    pass


class SpecAssignmentAdmin(admin.ModelAdmin):
    pass


class MajorTestAdmin(admin.ModelAdmin):
    pass


class SpecTestAdmin(admin.ModelAdmin):
    pass


class MajorStatAdmin(admin.ModelAdmin):
    pass


class MajorCourseStatAdmin(admin.ModelAdmin):
    pass


class SpecCourseStatAdmin(admin.ModelAdmin):
    pass


class SpecStatAdmin(admin.ModelAdmin):
    pass


admin.site.register(Student, StudentAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(Spec, SpecAdmin)
admin.site.register(MajorCourse, MajorCourseAdmin)
admin.site.register(SpecCourse, SpecCourseAdmin)
admin.site.register(MajorAssignment, MajorAssignmentAdmin)
admin.site.register(SpecAssignment, SpecAssignmentAdmin)
admin.site.register(MajorTest, MajorTestAdmin)
admin.site.register(SpecTest, SpecTestAdmin)
admin.site.register(MajorStat, MajorStatAdmin)
admin.site.register(MajorCourseStat, MajorCourseStatAdmin)
admin.site.register(SpecCourseStat, SpecCourseStatAdmin)
admin.site.register(SpecStat, SpecStatAdmin)
