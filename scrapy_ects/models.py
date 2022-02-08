from django.db import models
from django.contrib.auth.models import User

"""To be updated/corrected
   -----------------------
None for now
"""

class Student(models.Model):
    """Student model servers purpose of User's unique info.

    Attributes
    ----------
    current_sem: 
        Optional mint. Student's current semester he is attending.
    album_nr:
        Mint. Student's album number.

    Relations
    ---------
    o2o:
        user:
            User model.
    2m2:
        major:
            Major model through MajorStat.
        spec_stat:
            Spec model through SpecStat.
        major_course:
            MajorCourse model through MajorCourseStat.
        spec_course:
            SpecCourse model through SpecCourseStat.

    Constraints
    -----------
    models.UniqueConstraint:
        Instances can't be duplicated in album_nr attribute.
    """

    current_sem = models.IntegerField(blank=True, null=True)
    album_nr = models.IntegerField(null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    major = models.ManyToManyField('Major', through='MajorStat')
    spec = models.ManyToManyField('Spec', through='SpecStat')
    major_course = models.ManyToManyField(
        'MajorCourse', through='MajorCourseStat')
    spec_course = models.ManyToManyField(
        'SpecCourse', through='SpecCourseStat', blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __repr__(self):
        return f'Student(id={self.id}, current_sem={self.current_sem}, album_nr={self.album_nr}, user={self.user}, major={self.major}, spec={self.spec}, major_course={self.major_course}, spec_course={self.spec_course})'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['album_nr'], name='unique_student')
        ]
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Major(models.Model):
    """Major model serves purpose of majors pool.

    Attributes
    ----------
    name:
        Mchar. Major's name.
    duration_in_sem:
        Optional mint. Major's duration in semester units.

    Constraints
    -----------
    models.UniqueConstraint:
        Instances can't be duplicated in name and duration_in_sem attributes.
    """

    name = models.CharField(max_length=128)
    duration_in_sem = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Major(id={self.id}, name="{self.name}", duration_in_sem={self.duration_in_sem})'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'duration_in_sem'], name='unique_major')
        ]
        verbose_name = 'Major'
        verbose_name_plural = 'Majors'


class Spec(models.Model):
    """Spec model serves purpose of Major's specializations pool.

    Attributes
    ----------
    name:
        Mchar. Specialization's name.

    Relations
    ---------
    fk:
        major:
            Major model.

    Constraints
    -----------
    models.UniqueConstraint:
        Instances can't be duplicated in name and major attributes.
    """

    name = models.CharField(max_length=128)
    major = models.ForeignKey('Major', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Major(id={self.id}, name="{self.name}", major={self.major})'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'major'], name='unique_spec')
        ]
        verbose_name = 'Spec'
        verbose_name_plural = 'Specs'


class AbstractCourse(models.Model):
    """Abstract AbstractCourse model for MajorCourseStat and SpecCourseStat.

    Attributes
    ----------
    ects:
        Mint. Course's ects to gain.
    course_passed:
        Mbool. Is the course already passed.
    degree:
        Mfloat. Course's degree of accomplishment.

    Relations
    ---------
    fk:
        student:
            Student model.
    """
    ects = models.IntegerField(default=0)
    course_passed = models.BooleanField(default=False)
    degree = models.FloatField(default=0.0)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    semester = models.IntegerField()
    lecturer = models.CharField(max_length=128, blank=True, null=True)
    sylabus = models.FileField(blank=True, null=True)
    total_points = models.IntegerField(default=100)
    total_points_scored = models.IntegerField(blank=True, null=True)


    class Meta:
        abstract = True
        verbose_name = 'AbstractCourse'
        verbose_name_plural = 'AbstractCourses'


class MajorCourseStat(AbstractCourse):
    """MajorCourseStat model, inheriting from AbstractCourse model, serves purpose of User's 
    major's course's unique info as intermediate table between Student and MajorCourse models.

    Attributes
    ----------
    ects:
        Mint. Course's ects to gain.
    course_passed:
        Mbool. Is the course already passed.
    degree:
        Mfloat. Course's degree of accomplishment.

    Relations
    ---------
    fk:
        student:
            Student model.
        major_course:
            MajorCourse model.
    """

    major_course = models.ForeignKey('MajorCourse', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.major_course.name}'

    def __repr__(self):
        return f'MajorCourseStat(id={self.id}, ects={self.ects}, course_passed={self.course_passed}, degree={self.degree}, student={self.student}, major_course={self.major_course})'

    class Meta:

        verbose_name = 'MajorCourseStat'
        verbose_name_plural = 'MajorCourseStats'


class SpecCourseStat(AbstractCourse):
    """SpecCourseStat model, inheriting from AbstractCourse model, serves purpose of User's 
    specialization's course's unique info as intermediate table between Student and SpecCourse models.

    Attributes
    ----------
    ects:
        Mint. Course's ects to gain.
    course_passed:
        Mbool. Is the course already passed.
    degree:
        Mfloat. Course's degree of accomplishment.

    Relations
    ---------
    fk:
        student:
            Student model.
        spec_course:
            SpecCourse model.
    """

    spec_course = models.ForeignKey('SpecCourse', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.spec_course.name}'

    def __repr__(self):
        return f'SpecCourseStat(id={self.id}, ects={self.ects}, course_passed={self.course_passed}, degree={self.degree}, student={self.student}, spec_course={self.spec_course})'

    class Meta:
        verbose_name = 'SpecCourseStat'
        verbose_name_plural = 'SpecCourseStats'


class MajorCourse(models.Model):
    """MajorCourse model serves purpose of major's courses pool.

    Attributes
    ----------
    name:
        Mchar. Course's name.

    Relations
    ---------
    fk:
        major:
            Major model.

    Constraints
    -----------
    models.UniqueConstraint:
        Instances can't be duplicated in name and major attributes.
    """
    name = models.CharField(max_length=128)
    major = models.ForeignKey('major', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'MajorCourse(id={self.id}, name="{self.name}", major={self.major})'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'major'], name='unique_major_course')
        ]
        verbose_name = 'MajorCourse'
        verbose_name_plural = 'MajorCourses'


class SpecCourse(models.Model):
    """SpecCourse model serves purpose of spec's courses pool.

    Attributes
    ----------
    name:
        Mchar. Course's name.

    Relations
    ---------
    fk:
        spec:
            Spec model.

    Constraints
    -----------
    models.UniqueConstraint:
        Instances can't be duplicated in name and spec attributes.
    """
    name = models.CharField(max_length=128)
    spec = models.ForeignKey('Spec', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'SpecCourse(id={self.id}, name="{self.name}", spec={self.spec})'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'spec'], name='unique_spec_course')
        ]
        verbose_name = 'SpecCourse'
        verbose_name_plural = 'SpecCourses'


class AbstractAssignmentTest(models.Model):
    """Abstract AbstractAssignment model for MajorAssignment and SpecAssignment.

    Attributes
    ----------
    name:
        Mchar. Assignment's name.
    max_points:
        Mfloat. Assignment's maximum points to score from.
    points:
        Optional mfloat. Assignment's points scored.
    more_info:
        Optional mtext. Assignment's instructions.
    """

    name = models.CharField(max_length=128)
    max_points = models.FloatField()
    points = models.FloatField(default=0)
    more_info = models.TextField(blank=True)
    has_date = models.BooleanField()
    the_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = 'AbstractAssignmentTest'
        verbose_name_plural = 'AbstractAssignmentsTests'


class MajorAssignment(AbstractAssignmentTest):
    """MajorAssignment model, inheriting from AbstractAssignment model, serves purpose of User's 
    course's assignment's unique info.

    Attributes
    ----------
    name:
        Mchar. Assignment's name.
    max_points:
        Mfloat. Assignment's maximum points to score from.
    points:
        Optional mfloat. Assignment's points scored.
    more_info:
        Optional mtext. Assignment's instructions.

    Relations
    ---------
    fk:
        major_course_stat:
            MajorCourseStat model.      
    """

    course_stat = models.ForeignKey(
        'MajorCourseStat', on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f'MajorAssignment(id={self.id}, name="{self.name}", max_points={self.max_points}, points={self.points}, more_info="{self.more_info}", major_course_stat={self.course_stat})'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(has_date__exact=True, the_date__isnull=False) | models.Q(has_date__exact=False, the_date__isnull=True)), name='the_major_date_check'),
        ]
        verbose_name = 'MajorAssignment'
        verbose_name_plural = 'MajorAssignments'


class SpecAssignment(AbstractAssignmentTest):
    """SpecAssignment model, inheriting from AbstractAssignment model, serves purpose of User's 
    course's assignment's unique info.

    Attributes
    ----------
    name:
        Mchar. Assignment's name.
    max_points:
        Mfloat. Assignment's maximum points to score from.
    points:
        Optional mfloat. Assignment's points scored.
    more_info:
        Optional mtext. Assignment's instructions.

    Relations
    ---------
    fk:
        spec_course_stat:
            SpecCourseStat model.
    """

    course_stat = models.ForeignKey(
        'SpecCourseStat', on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f'SpecAssignment(id={self.id}, name="{self.name}", max_points={self.max_points}, points={self.points}, more_info="{self.more_info}", spec_course_stat={self.course_stat})'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(has_date=True, the_date__isnull=False) | models.Q(has_date=False, the_date__isnull=True)), name='the_spec_date_check'),
        ]
        verbose_name = 'SpecAssignment'
        verbose_name_plural = 'SpecAssignments'


# class AbstractTest(models.Model):
#     """Abstract AbstractTest model for MajorTest and SpecTest.

#     Attributes
#     ----------
#     name:
#         Mchar. Assignment's name.
#     max_points:
#         Mfloat. Assignment's maximum points to score from.
#     points:
#         Optional mfloat. Assignment's points scored.
#     more_info:
#         Optional mtext. Assignment's instructions.
#     """

#     name = models.CharField(max_length=128)
#     max_points = models.IntegerField()
#     points = models.IntegerField(blank=True)
#     more_info = models.TextField()

#     def __str__(self):
#         return self.name

#     class Meta:
#         abstract = True
#         verbose_name = 'AbstractTest'
#         verbose_name_plural = 'AbstractTests'


class MajorTest(AbstractAssignmentTest):
    """MajorTest model, inheriting from AbstractTest model, serves purpose of User's 
    course's test's unique info.

    Attributes
    ----------
    name:
        Mchar. Test's name.
    max_points:
        Mfloat. Test's maximum points to score from.
    points:
        Optional mfloat. Test's points scored.
    more_info:
        Optional mtext. Test's instructions.

    Relations
    ---------
    fk:
        major_course_stat:
            MajorCourseStat model.
    """

    course_stat = models.ForeignKey(
        'MajorCourseStat', on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f'MajorTest(id={self.id}, name="{self.name}", max_points={self.max_points}, points={self.points}, more_info="{self.more_info}", major_course_stat={self.course_stat})'

    class Meta:
        verbose_name = 'MajorTest'
        verbose_name_plural = 'MajorTests'


class SpecTest(AbstractAssignmentTest):
    """SpecTest model, inheriting from AbstractTest model, serves purpose of User's 
    course's test's unique info.

    Attributes
    ----------
    name:
        Mchar. Test's name.
    max_points:
        Mfloat. Test's maximum points to score from.
    points:
        Optional mfloat. Test's points scored.
    more_info:
        Optional mtext. Test's instructions.

    Relations
    ---------
    fk:
        spec_course_stat:
            SpecCourseStat model.
    """

    course_stat = models.ForeignKey(
        'SpecCourseStat', on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f'SpecTest(id={self.id}, name="{self.name}", max_points={self.max_points}, points={self.points}, more_info="{self.more_info}", spec_course_stat={self.course_stat})'

    class Meta:
        verbose_name = 'SpecTest'
        verbose_name_plural = 'SpecTests'


class MajorStat(models.Model):
    """MajorStat model serves purpose of User's major's unique info 
    as intermediate table between Student and Major models.

    Attributes
    ----------
    max_ects:
        Mint. Major's ects points to score.
    current_ects:
        Optional mint. Major's current ects points scored.
    start_of_major:
        Mdate. Major's start date.
    department:
        Optional mchar. Major's department name.

    Relations
    ---------
    fk:
        student:
            Student model.
        major:
            Major model.
    """

    max_ects = models.IntegerField(default=210)
    current_ects = models.IntegerField(blank=True, null=True)
    start_of_major = models.DateField(auto_now=True)
    department = models.CharField(max_length=128, blank=True, null=True)

    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    major = models.ForeignKey('Major', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.major}'
    
    def __repr__(self):
        return f'MajorStat(id={self.id}, max_ects={self.max_ects}, current_ects={self.current_ects}, start_of_major={self.start_of_major}, department="{self.department}", student={self.student}, major={self.major})'

    class Meta:
        verbose_name = 'MajorStat'
        verbose_name_plural = 'MajorStats'


class SpecStat(models.Model):
    """SpecStat model serves purpose of User's spec's unique info 
    as intermediate table between Student and Spec models.

    Relations
    ---------
    fk:
        student:
            Student model.
        spec:
            Spec model.
    """

    spec = models.ForeignKey('Spec', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.spec}'

    def __repr__(self):
        return f'SpecStat(id={self.id}, student={self.student}, spec={self.spec})'

    class Meta:
        verbose_name = 'SpecStat'
        verbose_name_plural = 'SpecStats'
