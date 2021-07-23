from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, UserAvatar, PICTURE_VARIATIONS


class StdImageField(serializers.ImageField):
    def to_native(self, obj):
        return self.get_variations_urls(obj)

    def get_variations_urls(self, obj):
        return_object = {}
        field = obj.field
        if hasattr(field, 'variations'):
            variations = field.variations
            for key, attr in variations.iteritems():
                if hasattr(obj, key):
                    fieldObj = getattr(obj, key, None)
                    if fieldObj:
                        url = getattr(fieldObj, 'url', None)
                        if url:
                            return_object[key] = url

        if hasattr(obj, 'url'):
            return_object['original'] = obj.url

        return return_object

    def from_native(self, data):
        return super(serializers.ImageField, self).from_native(data)


class AvatarSerializer(serializers.ModelSerializer):
    file = StdImageField()

    class Meta:
        model = UserAvatar
        fields = ('file', 'name',)

    def to_representation(self, instance):
        # return self.fields['file'].to_representation(instance.file)
        # ans = {}
        # for i, item in enumerate(PICTURE_VARIATIONS):
        #     print(item)
        #     ans.update({f'{item}': instance.file[item].url})
        print(self.context['request'].META['wsgi.url_scheme']+'://'+self.context['request'].META['HTTP_HOST'])
        return {'name': instance.name,
                'orig': instance.file.url,
                'small': instance.file.small.url,
                'profile': instance.file.profile.url,
                'url': self.context['request'].META['wsgi.url_scheme']+'://'+self.context['request'].META['HTTP_HOST']}


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    # Убедитесь, что пароль содержит не менее 8 символов, не более 128,
    # и так же что он не может быть прочитан клиентской стороной
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # Клиентская сторона не должна иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.
    token = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    avatar = AvatarSerializer(many=False, read_only=True)
    class Meta:
        model = User
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['email','token', 'username', 'is_active', 'password', 'lastName', 'firstName', 'vkLink', 'avatar', 'phone',]

    def create(self, validated_data):
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # В методе validate мы убеждаемся, что текущий экземпляр
        # LoginSerializer значение valid. В случае входа пользователя в систему
        # это означает подтверждение того, что присутствуют адрес электронной
        # почты и то, что эта комбинация соответствует одному из пользователей.
        email = data.get('email', None)
        password = data.get('password', None)

        # Вызвать исключение, если не предоставлена почта.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Вызвать исключение, если не предоставлен пароль.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # Метод authenticate предоставляется Django и выполняет проверку, что
        # предоставленные почта и пароль соответствуют какому-то пользователю в
        # нашей базе данных. Мы передаем email как username, так как в модели
        # пользователя USERNAME_FIELD = email.
        user = authenticate(username=email, password=password)

        # Если пользователь с данными почтой/паролем не найден, то authenticate
        # вернет None. Возбудить исключение в таком случае.
        if user is None:
            raise serializers.ValidationError(
                'Пользователь с этим адресом электронной почты и паролем не найден.'
            )

        # Django предоставляет флаг is_active для модели User. Его цель
        # сообщить, был ли пользователь деактивирован или заблокирован.
        # Проверить стоит, вызвать исключение в случае True.
        if not user.is_active:
            raise serializers.ValidationError(
                'Этот пользователь был деактивирован.'
            )

        # Метод validate должен возвращать словать проверенных данных. Это
        # данные, которые передются в т.ч. в методы create и update.
        return {
            # 'email': user.email,
            # 'username': user.username,
            'token': user.token,
        }


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов User. """

    # Пароль должен содержать от 8 до 128 символов. Это стандартное правило. Мы
    # могли бы переопределить это по-своему, но это создаст лишнюю работу для
    # нас, не добавляя реальных преимуществ, потому оставим все как есть.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    avatar = AvatarSerializer(many=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'is_active', 'password', 'lastName', 'firstName', 'vkLink', 'avatar', 'phone',)

        # Параметр read_only_fields является альтернативой явному указанию поля
        # с помощью read_only = True, как мы это делали для пароля выше.
        # Причина, по которой мы хотим использовать здесь 'read_only_fields'
        # состоит в том, что нам не нужно ничего указывать о поле. В поле
        # пароля требуются свойства min_length и max_length,
        # но это не относится к полю токена.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """ Выполняет обновление User. """
        # В отличие от других полей, пароли не следует обрабатывать с помощью
        # setattr. Django предоставляет функцию, которая обрабатывает пароли
        # хешированием и 'солением'. Это означает, что нам нужно удалить поле
        # пароля из словаря 'validated_data' перед его использованием далее.
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            # Для ключей, оставшихся в validated_data мы устанавливаем значения
            # в текущий экземпляр User по одному.
            setattr(instance, key, value)

        if password is not None:
            # 'set_password()' решает все вопросы, связанные с безопасностью
            # при обновлении пароля, потому нам не нужно беспокоиться об этом.
            instance.set_password(password)
        instance.save()

        return instance


class UserDataSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов User. """
    avatar = AvatarSerializer(many=False)
    class Meta:
        model = User
        fields = ('email', 'username', 'is_active', 'firstName', 'lastName', 'vkLink', 'avatar', 'phone')

    # def get_avatar(self, User):
    #     data = {}
    #     data.update(id=User.avatar.id)
    #     data.update(link=User.avatar.link)
    #     data.update(file=User.avatar.file_link)
    #     data.update(name=User.avatar.name)
    #     return data


class AvatarUploaderSerializer(serializers.Serializer):
    file = StdImageField()
    # file_50x50 = serializers.FileField(read_only=True)
    # file_200x200 = serializers.FileField(read_only=True)
    name = serializers.CharField(max_length=255, read_only=True)

    def validate(self, validated_data):
        validated_data['size'] = validated_data['file'].size
        validated_data['name'] = validated_data['file'].name
        # validated_data['file_50x50'] = validated_data['file']
        # validated_data['file_200x200'] = validated_data['file']
        return validated_data

    def create(self, validated_data):
        AvatarUploader_object = UserAvatar.objects.create(**validated_data)
        AvatarUploader_object.save()
        userObject = User.objects.get(id=self.context['request'].user.id)
        userObject.avatar_id = AvatarUploader_object
        userObject.save()
        return AvatarUploader_object

    class Meta:
        model = UserAvatar
        fields = ('file')
        read_only_fields = ('name', 'file',)
