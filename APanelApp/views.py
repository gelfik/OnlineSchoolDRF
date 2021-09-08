from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from APanelApp.service import CoursesListFilter
from CoursesApp.models import CoursesListModel, CoursesPredmetModel, CoursesTypeModel, CoursesExamTypeModel
from CoursesApp.serializers import CoursesForApanelListSerializer, CoursesAddCourseSerializer, CoursesMetadataSerializer


class APanelCoursesListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = CoursesForApanelListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CoursesListFilter
    pagination_class = None

    def get_queryset(self):
        CoursesList_object = CoursesListModel.objects.order_by('id').filter(is_active=True, teacher__user=self.request.user)
        return CoursesList_object

class APanelCoursesAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CoursesAddCourseSerializer
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        # user = request.data.get('user', {})
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data:
                serializer_data.update({f'{item}': data})
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=serializer_data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': True, 'id': serializer.data['id']}, status=status.HTTP_201_CREATED)


class APanelCoursesMetadataAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        serializer = CoursesMetadataSerializer({
            'predmet': CoursesPredmetModel.objects.filter(is_active=True),
            'courseType': CoursesTypeModel.objects.filter(is_active=True),
            'examType': CoursesExamTypeModel.objects.filter(is_active=True)
        })
        return Response(serializer.data, status=status.HTTP_200_OK)
