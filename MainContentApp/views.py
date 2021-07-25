from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

from .serializers import (TeacherDataSerializer, EducationDataSerializer)
from .models import TeacherList
# Create your views here.

class TeacherDataAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = TeacherDataSerializer

    def get_queryset(self):
        return TeacherList.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        TeacherList_objects = self.get_queryset()
        serializer = TeacherDataSerializer(TeacherList_objects, many=True, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class EducationDataAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = EducationDataSerializer

    def get_queryset(self):
        return TeacherList.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        EducationList_objects = self.get_queryset()
        serializer = EducationDataSerializer(EducationList_objects, many=True, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)