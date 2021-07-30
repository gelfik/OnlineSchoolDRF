import os, uuid

from django.db import models
from stdimage import StdImageField
from stdimage.validators import MaxSizeValidator

# Create your models here.
# from CoursesApp.models import CoursesNameModel

PICTURE_VARIATIONS = {
    'small': dict(width=64, height=64, crop=True),
    'profile': dict(width=400, height=400, crop=True),
}


class AvatarModel(models.Model):
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
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Фото преподавателя'
        verbose_name_plural = 'Фото преподавателей'
        db_table = 'TeachersAvatar'

    def __str__(self):
        return str(self.file)


class LinkModel(models.Model):
    vk = models.CharField('Ссылка Vk', default=None, max_length=255, null=True, blank=True)
    instagram = models.CharField('Ссылка instagram', default=None, max_length=255, null=True, blank=True)
    youtube = models.CharField('Ссылка Youtube', default=None, max_length=255, null=True, blank=True)
    telegram = models.CharField('Ссылка Telegram', default=None, max_length=255, null=True, blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Ссылки на препода'
        verbose_name_plural = 'Ссылки на препода'
        db_table = 'TeachersLink'

    def __str__(self):
        return f'{self.vk}'


class TeachersModel(models.Model):
    lastName = models.CharField('Фамилия препода', default=None, max_length=255)
    firstName = models.CharField('Имя препода', default=None, max_length=255)
    subject = models.CharField('Предмет', default=None, max_length=255)
    # subject = models.ForeignKey(CoursesNameModel, on_delete=models.CASCADE, verbose_name='Предмет',
    #                             default=None, null=True)
    addDate = models.DateTimeField('Дата добавления', auto_now=True, db_index=True)
    shortDescription = models.CharField('Краткое описание', default=None, max_length=255)
    description = models.TextField('Описание', default=None)
    teacherLink = models.ForeignKey(LinkModel, on_delete=models.CASCADE, verbose_name='Ссылки на препода',
                                    default=None, null=True)
    avatar = models.ForeignKey(AvatarModel, on_delete=models.CASCADE, verbose_name='Фото преподавателя', default=None,
                               null=True,
                               blank=True)
    is_active = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        db_table = 'TeachersTeachers'

    def __str__(self):
        return f'{self.lastName} {self.firstName}'