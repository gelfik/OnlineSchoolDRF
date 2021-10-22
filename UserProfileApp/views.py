from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserAvatar
from .renderers import UserJSONRenderer
from .serializers import (LoginSerializer, RegistrationSerializer, UserRetrieveUpdateSerializer, UserDataSerializer,
                          AvatarUploaderSerializer, )


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        # user = request.data.get('user', {})
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=serializer_data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        # user = request.data.get('user', {})
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = {'email': email, 'password': password}
        # Обратите внимание, что мы не вызываем метод save() сериализатора, как
        # делали это для регистрации. Дело в том, что в данном случае нам
        # нечего сохранять. Вместо этого, метод validate() делает все нужное.
        serializer = self.serializer_class(data=user, context={'request': self.request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserRetrieveUpdateSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(request.user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        serializer = self.serializer_class(request.user, data=serializer_data, partial=True, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDataAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserDataSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data={'user': request.user}, partial=True, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class SetUserAvatarAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    # parser_classes = (FileUploadParser, )
    serializer_class = AvatarUploaderSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.FILES, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
