import os
import uuid
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from stdimage import StdImageField
from stdimage.validators import MaxSizeValidator


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
        return str(self.name)


# class UserAvatar(models.Model):
#     def get_file_path_200x200(instance, filename):
#         ext = filename.split('.')[-1]
#         filename = "%s_200x200.%s" % (uuid.uuid4(), ext)
#         return os.path.join('avatar', filename)
#
#     def get_file_path_orig(instance, filename):
#         ext = filename.split('.')[-1]
#         filename = "%s_orig.%s" % (uuid.uuid4(), ext)
#         return os.path.join('avatar', filename)
#
#     def get_file_path_50x50(instance, filename):
#         ext = filename.split('.')[-1]
#         filename = "%s_50x50.%s" % (uuid.uuid4(), ext)
#         return os.path.join('avatar', filename)
#
#     def get_file_path(instance, filename):
#         ext = filename.split('.')[-1]
#         filename = "%s_orig.%s" % (uuid.uuid4(), ext)
#         return os.path.join('avatar', filename)
#
#     # file_link = get_file_path
#     new = uuid.uuid4()
#     file = models.FileField('Файл оригинал', upload_to=get_file_path_orig, null=True, blank=True, unique=True)
#     file_200x200 = ResizedImageField('Файл 200x200', size=[200, 200], quality=100, upload_to=get_file_path_200x200,
#                                      null=True,
#                                      blank=True, unique=True)
#     file_50x50 = ResizedImageField('Файл 50x50', size=[50, 50], quality=100, upload_to=get_file_path_50x50,
#                                    null=True,
#                                    blank=True, unique=True)
#     name = models.CharField('Название', default=None, max_length=255,
#                             blank=False)  # name is filename without extension
#     upload_date = models.DateTimeField('Дата загрузки', auto_now=True, db_index=True)
#     size = models.IntegerField('Размер', default=0)
#     is_active = models.BooleanField('Статус удаления', default=True)
#
#     class Meta:
#         verbose_name = 'Аватар'
#         verbose_name_plural = 'Аватары'
#         db_table = 'UserAvatar'
#
#     def __str__(self):
#         return str(self.name)


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
        user.firstName = firstName
        user.lastName = lastName
        user.vkLink = vkLink
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Каждому пользователю нужен понятный человеку уникальный идентификатор,
    # который мы можем использовать для предоставления User в пользовательском
    # интерфейсе. Мы так же проиндексируем этот столбец в базе данных для
    # повышения скорости поиска в дальнейшем.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # Так же мы нуждаемся в поле, с помощью которого будем иметь возможность
    # связаться с пользователем и идентифицировать его при входе в систему.
    # Поскольку адрес почты нам нужен в любом случае, мы также будем
    # использовать его для входы в систему, так как это наиболее
    # распространенная форма учетных данных на данный момент (ну еще телефон).
    email = models.EmailField(db_index=True, unique=True)

    # Когда пользователь более не желает пользоваться нашей системой, он может
    # захотеть удалить свой аккаунт. Для нас это проблема, так как собираемые
    # нами данные очень ценны, и мы не хотим их удалять :) Мы просто предложим
    # пользователям способ деактивировать учетку вместо ее полного удаления.
    # Таким образом, они не будут отображаться на сайте, но мы все еще сможем
    # далее анализировать информацию.
    is_active = models.BooleanField(default=True)

    # Этот флаг определяет, кто может войти в административную часть нашего
    # сайта. Для большинства пользователей это флаг будет ложным.
    is_staff = models.BooleanField(default=False)

    # Временная метка создания объекта.
    created_at = models.DateTimeField(auto_now_add=True)

    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(auto_now=True)

    # Дополнительный поля, необходимые Django
    # при указании кастомной модели пользователя.
    lastName = models.CharField('Фамилия', max_length=255, default=None, null=True)
    firstName = models.CharField('Имя', max_length=255, default=None, null=True)
    patronymic = models.CharField('Отчество', max_length=255, default=None, null=True)
    phone = models.CharField('Телефон', max_length=255, default=None, null=True)
    vkLink = models.CharField('Ссылка на вк', max_length=255, default=None, null=True)

    avatar = models.ForeignKey(UserAvatar, on_delete=models.CASCADE, verbose_name='Аватар', default=0, null=True,
                               blank=True)

    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()

    # @property
    # def avatar(self):
    #     data = {}
    #     data.update(id=self.avatar.id)
    #     data.update(link=self.avatar.link)
    #     data.update(file=self.avatar.file_link)
    #     data.update(name=self.avatar.name)
    #     return data

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'Users'

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.email

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
