from django.contrib import admin
from .models import CoursesTypeModel, CoursesPredmetModel, CoursesExamTypeModel, CoursesListModel, \
    CoursesSubCoursesModel


# Register your models here.

@admin.register(CoursesExamTypeModel)
class CoursesExamType(admin.ModelAdmin):
    list_display = ('name', 'is_active',)


@admin.register(CoursesPredmetModel)
class CoursesPredmet(admin.ModelAdmin):
    list_display = ('name', 'is_active',)


@admin.register(CoursesTypeModel)
class CoursesName(admin.ModelAdmin):
    list_display = ('name', 'id', 'shortDescription', 'duration', 'durationCount', 'recruitmentStatus', 'is_active',)


@admin.register(CoursesSubCoursesModel)
class CoursesSubCourses(admin.ModelAdmin):
    list_display = ('name', 'id', 'startDate', 'endDate', 'is_active',)


@admin.register(CoursesListModel)
class CoursesList(admin.ModelAdmin):
    list_display = ('predmet', 'id', 'courseType', 'courseExamType', 'teacher', 'price', 'is_active',)
