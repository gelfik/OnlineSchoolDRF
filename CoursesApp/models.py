from django.db import models

# Create your models here.
# import TeachersApp.models
from TeachersApp.models import TeachersModel

import TeachersApp

class CoursesExamTypeModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Тип экзамена'
        verbose_name_plural = 'Типы экзаменов'
        db_table = 'CoursesExamType'

    def __str__(self):
        return f'{self.name}'

class CoursesPredmetModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        db_table = 'CoursesPredmet'

    def __str__(self):
        return f'{self.name}'

class CoursesNameModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Название курса'
        verbose_name_plural = 'Названия курсов'
        db_table = 'CoursesName'

    def __str__(self):
        return f'{self.name}'

class CoursesListModel(models.Model):
    predmet = models.ForeignKey(CoursesPredmetModel, on_delete=models.CASCADE, verbose_name='Предмет',
                                    default=None, null=True)
    courseName = models.ForeignKey(CoursesNameModel, on_delete=models.CASCADE, verbose_name='Тип курса',
                                default=None, null=True)
    courseExamType = models.ForeignKey(CoursesExamTypeModel, on_delete=models.CASCADE, verbose_name='Тип курса',
                                   default=None, null=True)
    teacher = models.ForeignKey(TeachersModel, on_delete=models.CASCADE, verbose_name='Преподаватель',
                                   default=None, null=True)
    price = models.FloatField('Цена', default=0)

    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Список курсов'
        db_table = 'CoursesList'

    def __str__(self):
        return f'{self.courseName} {self.predmet} {self.courseExamType}'