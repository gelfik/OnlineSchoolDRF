from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CoursesListSerializer, FilterDataSerializer, CoursesDetailSerializer
from .models import CoursesListModel, CoursesExamTypeModel, CoursesPredmetModel, CoursesTypeModel
from .service import CoursesListFilter, PaginationCourses

class FilterDataAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        serializer = FilterDataSerializer({
            'predmet': CoursesPredmetModel.objects.filter(is_active=True),
            'courseType': CoursesTypeModel.objects.filter(is_active=True),
            'examType': CoursesExamTypeModel.objects.filter(is_active=True)
        })

        return Response(serializer.data, status=status.HTTP_200_OK)


class CoursesListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CoursesListFilter
    pagination_class = PaginationCourses

    def get_queryset(self):
        CoursesList_object = CoursesListModel.objects.order_by('id').filter(is_active=True)
        return CoursesList_object


class CourseDetailAPIView(RetrieveAPIView):
    queryset = CoursesListModel.objects.all().order_by('id').filter(is_active=True)
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesDetailSerializer
    pagination_class = None

    # def get_queryset(self):
    #     CoursesList_object = CoursesListModel.objects.order_by('id').filter(is_active=True)
    #     return CoursesList_object