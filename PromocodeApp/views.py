import datetime

from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status
# Create your views here.
from .models import PromocodeListModel
from .serializers import PromocodeSerializer


class PromocodeDataAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        promocode = request.data.get('promocode', None)
        if promocode:
            try:
                promocode_object = PromocodeListModel.objects.get(is_active=True, promocode=promocode)
            except:
                return Response({'error': 'Промокод не найден!'}, status=status.HTTP_200_OK)
            if datetime.datetime.strptime(str(promocode_object.validDate), "%Y-%m-%d") < datetime.datetime.now() - datetime.timedelta(days=1):
                return Response({'error': 'Истек срок действия промокода'}, status=status.HTTP_200_OK)
            if promocode_object.promocodeCount > promocode_object.activeCount:
                return Response({'promocode': promocode_object.promocode, 'type': promocode_object.type.name,
                                 'count': promocode_object.count}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Использовано максимальное число промокодов'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Вы не отправили промокод'}, status=status.HTTP_200_OK)