import os, uuid

from django.db import models
from stdimage import StdImageField
from stdimage.validators import MaxSizeValidator

# Create your models here.

PICTURE_VARIATIONS = {
    'small': dict(width=64, height=64, crop=True),
    'profile': dict(width=400, height=400, crop=True),
}


class TeacherAvatar(models.Model):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('main', filename)

    max_width = 5000
    max_height = 7000

    file = StdImageField(
        verbose_name='Изображение',
        upload_to=get_file_path,
        variations=PICTURE_VARIATIONS,
        validators=[MaxSizeValidator(max_width, max_height)],
    )
    name = models.CharField('Название', default=None, max_length=255, blank=False)
    upload_date = models.DateTimeField('Дата загрузки', auto_now=True, db_index=True)
    size = models.IntegerField('Размер', default=0)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Фото преподавателя'
        verbose_name_plural = 'Фото преподавателей'
        db_table = 'TeacherAvatar'

    def __str__(self):
        return str(self.name)


class ExamType(models.Model):
    name = models.CharField('Тип экзамена', default=None, max_length=255)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Тип экзамена'
        verbose_name_plural = 'Типы экзаменов'
        db_table = 'ExamType'

    def __str__(self):
        return f'{self.name}'



class TeacherLink(models.Model):
    vk = models.CharField('Ссылка Vk', default=None, max_length=255, null=True, blank=True)
    instagram = models.CharField('Ссылка instagram', default=None, max_length=255, null=True, blank=True)
    youtube = models.CharField('Ссылка Youtube', default=None, max_length=255, null=True, blank=True)
    telegram = models.CharField('Ссылка Telegram', default=None, max_length=255, null=True, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Ссылки на препода'
        verbose_name_plural = 'Ссылки на препода'
        db_table = 'TeacherLink'

    def __str__(self):
        return f'{self.vk}'

class TeacherList(models.Model):
    lastName = models.CharField('Фамилия препода', default=None, max_length=255)
    firstName = models.CharField('Имя препода', default=None, max_length=255)
    subject = models.CharField('Предмет', default=None, max_length=255)
    add_date = models.DateTimeField('Дата добавления', auto_now=True, db_index=True)
    shortDescription = models.CharField('Краткое описание', default=None, max_length=255)
    description = models.TextField('Описание', default=None)
    examType = models.ForeignKey(ExamType, on_delete=models.CASCADE, verbose_name='Тип экзамена', default=None)
    teacherLink = models.ForeignKey(TeacherLink, on_delete=models.CASCADE, verbose_name='Ссылки на препода', default=None, null=True)
    avatar = models.ForeignKey(TeacherAvatar, on_delete=models.CASCADE, verbose_name='Фото преподавателя', default=None,
                               null=True,
                               blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        db_table = 'TeacherList'

    def __str__(self):
        return f'{self.lastName} {self.firstName} {self.subject}'

class EducationDataType(models.Model):
    name = models.CharField('Тип даты курса', default=None, max_length=255)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Тип даты курса'
        verbose_name_plural = 'Типы даты курсов'
        db_table = 'EducationDataType'

    def __str__(self):
        return f'{self.name}'

class EducationList(models.Model):
    name = models.CharField('Название', default=None, max_length=255)
    add_date = models.DateTimeField('Дата добавления', auto_now=True, db_index=True)
    shortDescription = models.CharField('Краткое описание', default=None, max_length=255)
    description = models.TextField('Описание', default=None)
    educationDataType = models.ForeignKey(EducationDataType, on_delete=models.CASCADE, verbose_name='Тип даты курса', default=None)
    countDate = models.IntegerField('Число зависимое от типа даты курса', default=0)
    recruitmentStatus = models.BooleanField('Статус набора', default=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        db_table = 'EducationList'

    def __str__(self):
        return f'{self.name}'
