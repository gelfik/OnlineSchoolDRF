import os
import uuid
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from stdimage import StdImageField
from stdimage.validators import MaxSizeValidator
from django.contrib.auth.models import Group

def transliterate(name):
    slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'u', 'я': 'ja', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
              'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
              'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
              'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
              'Ю': 'U', 'Я': 'YA', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
              '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
              ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
              '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
              'Є': 'e', '—': ''}
    for key in slovar:
        name = name.replace(key, slovar[key])
    return name


PICTURE_VARIATIONS = {
    'small': dict(width=64, height=64, crop=True),
    'profile': dict(width=148, height=148, crop=True),
    'medium': dict(width=512, height=512),
    'large': dict(width=1024, height=1024),
}

class UserAvatar(models.Model):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('avatar', filename)

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
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватары'
        db_table = 'UserAvatar'

    def __str__(self):
        return str(self.file.url)

class UserManager(BaseUserManager):
    """
    Django требует, чтобы кастомные пользователи определяли свой собственный
    класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
    же самого кода, который Django использовал для создания User (для демонстрации).
    """

    def create_user(self, email, lastName, firstName, vkLink, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        # if username is None:
        #     raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Email обязательное поле.')
        if lastName is None:
            raise TypeError('Фамилия обязательное поле.')
        if firstName is None:
            raise TypeError('Имя обязательное поле.')
        if vkLink is None:
            raise TypeError('Ссылка вк обязательное поле.')

        new_username = transliterate(firstName[:1] + lastName)

        user = self.model(username=new_username, email=self.normalize_email(email))
        user.set_password(password)
        user.firstName = firstName
        user.lastName = lastName
        user.vkLink = vkLink
        user.save()
        groupObj, groupCreatedStatus = Group.objects.get_or_create(name='Пользователь')
        user.groups.add(groupObj)
        user.save()

        return user

    def create_superuser(self, email, lastName, firstName, vkLink, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if email is None:
            raise TypeError('Email обязательное поле.')
        if lastName is None:
            raise TypeError('Фамилия обязательное поле.')
        if firstName is None:
            raise TypeError('Имя обязательное поле.')
        if vkLink is None:
            raise TypeError('Ссылка вк обязательное поле.')
        if password is None:
            raise TypeError('Пароль обязательное поле.')

        Group.objects.get_or_create(name='Пользователь')
        Group.objects.get_or_create(name='Наставник')
        groupObj, groupCreatedStatus = Group.objects.get_or_create(name='Преподаватель')
        user = self.create_user(email, lastName, firstName, vkLink, password)
        user.groups.add(groupObj)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата последнего изменения', auto_now=True)
    lastName = models.CharField('Фамилия', max_length=255, default=None)
    firstName = models.CharField('Имя', max_length=255, default=None)
    phone = models.CharField('Телефон', max_length=255, default=None, null=True)
    vkLink = models.CharField('Ссылка на вк', max_length=255, default=None, null=True)
    avatar = models.ForeignKey(UserAvatar, on_delete=models.CASCADE, verbose_name='Аватар', default=0, null=True,
                               blank=True)
    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'lastName', 'firstName', 'phone', 'vkLink', ]

    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'Users'

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    @property
    def isTeacher(self):
        return self.groups.filter(name='Преподаватель').exists()

    @property
    def isMentor(self):
        return self.groups.filter(name='Наставник').exists()

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({'user_data': {'id': self.pk, 'username': self.username,
                                          'created_date': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))},
                            'exp': datetime.now() + timedelta(days=60),
                            'iat': datetime.now(),
                            }, settings.SECRET_KEY, algorithm='HS256')

        return token
