from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PurchaseListSerializer, PurchaseDetailSerializer
from .models import PurchaseListModel

from UserProfileApp.models import User


# Create your views here.


# class PurchaseDataAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#     renderer_classes = (JSONRenderer,)
#
#     def get(self, request, *args, **kwargs):
#         user = User.objects.get(pk=request.user.pk)
#         isTeacher = isMentor = isBuyUser = False
#         if len(user.coursesUserCourseList.all()) > 0:
#             isBuyUser = True
#         if len(user.coursesTeacherList.all()) > 0:
#             isTeacher = True
#         if len(user.coursesMentorList.all()) > 0:
#             isMentor = True
#
#         data = user.coursesUserCourseList.filter(id=1)
#         print(data)
#         serializer = CoursesDetail(data, many=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)


class PurchaseDataAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseListSerializer
    pagination_class = None

    def get_queryset(self):
        PurchaseList_object = PurchaseListModel.objects.order_by('id').filter(is_active=True, user=self.request.user)
        return PurchaseList_object


class PurchaseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PurchaseDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return PurchaseListModel.objects.order_by('id').filter(is_active=True, user=self.request.user)
