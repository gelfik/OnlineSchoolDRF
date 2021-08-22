import os, uuid

from django.db import models
from django.utils.timezone import now as django_datetime_now
from TeachersApp.models import TeachersModel
from LessonApp.models import LessonModel
from UserProfileApp.models import User

# from stdimage import StdImageField
from stdimage.validators import MaxSizeValidator


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


class CoursesTypeModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    svg = models.TextField('SVG', default=None, null=True, blank=True)
    shortDescription = models.CharField('Краткое описание', default=None, max_length=255)
    description = models.TextField('Описание', default=None)
    duration = models.CharField('Продолжительность курса', default=None, max_length=255, null=True)
    durationCount = models.PositiveSmallIntegerField('Продолжительность курса(число месяцев)', default=1, null=True,
                                                     blank=True)
    recruitmentStatus = models.BooleanField('Статус набора', default=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Тип курса'
        verbose_name_plural = 'Типы курсов'
        db_table = 'CoursesType'

    def __str__(self):
        return f'{self.name}'

class CoursesSubCoursesModel(models.Model):
    name = models.CharField('Название', default=None, max_length=255, null=True)
    startDate = models.DateField('Дата начала подкурса', default=django_datetime_now)
    endDate = models.DateField('Дата окончания подкурса', default=django_datetime_now)
    leasonList = models.ManyToManyField(LessonModel, 'Уроки', null=True, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Подкурс'
        verbose_name_plural = 'Подкурсы'
        db_table = 'CoursesSubCourses'

    def __str__(self):
        return f'{self.name} {self.startDate} - {self.endDate}'

class CoursesListModel(models.Model):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('coursePicture', filename)

    name = models.CharField('Название', default=None, max_length=255, null=True)
    predmet = models.ForeignKey(CoursesPredmetModel, on_delete=models.CASCADE, verbose_name='Предмет',
                                default=None, null=True)
    courseType = models.ForeignKey(CoursesTypeModel, on_delete=models.CASCADE, verbose_name='Тип курса',
                                   default=None, null=True)
    courseExamType = models.ForeignKey(CoursesExamTypeModel, on_delete=models.CASCADE, verbose_name='Тип курса',
                                       default=None, null=True)
    coursePicture = models.ImageField(upload_to=get_file_path, verbose_name='Картинка курса',
                                      validators=[MaxSizeValidator(500, 500)], default=None, null=True)
    teacher = models.ForeignKey(TeachersModel, on_delete=models.CASCADE, verbose_name='Преподаватель',
                                default=None, null=True)
    shortDescription = models.TextField('Краткое описание', default=None, null=True)
    description = models.TextField('Описание', default=None, null=True)
    subCourses = models.ManyToManyField(CoursesSubCoursesModel, verbose_name='Подкурсы', null=True, blank=True)
    price = models.FloatField('Цена за месяц', default=0)
    discountDuration = models.PositiveSmallIntegerField('Скидка за месяц при оплате за весь срок обучения в %',
                                                        default=0, null=True, blank=True)
    buyAllSubCourses = models.BooleanField('Покупка сразу всех курсов', default=False)
    draft = models.BooleanField('Черновик', default=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Список курсов'
        db_table = 'CoursesList'

    def __str__(self):
        return f'{self.courseType} {self.predmet} {self.courseExamType}'
