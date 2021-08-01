from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from LessonApp.models import LessonModel
from LessonApp.serializers import LessonSerializer


class LessonListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = LessonSerializer
    pagination_class = None

    def get_queryset(self):
        Lesson_object = LessonModel.objects.order_by('id').filter(is_active=True)
        return Lesson_object