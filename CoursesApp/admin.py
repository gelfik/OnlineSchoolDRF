from django.contrib import admin
from .models import CoursesNameModel, CoursesPredmetModel, CoursesExamTypeModel, CoursesListModel
# Register your models here.

@admin.register(CoursesExamTypeModel)
class CoursesExamType(admin.ModelAdmin):
    list_display = ('name', 'is_active',)

@admin.register(CoursesPredmetModel)
class CoursesPredmet(admin.ModelAdmin):
    list_display = ('name', 'is_active',)

@admin.register(CoursesNameModel)
class CoursesName(admin.ModelAdmin):
    list_display = ('name', 'is_active',)

@admin.register(CoursesListModel)
class CoursesList(admin.ModelAdmin):
    list_display = ('predmet', 'courseName','courseExamType', 'teacher','price', 'is_active',)