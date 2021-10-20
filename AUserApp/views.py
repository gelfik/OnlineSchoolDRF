from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from AUserApp.service import UserListFilter, PaginationUser
from UserProfileApp.models import User
from UserProfileApp.serializers import UserDataSerializer
from rest_framework import filters

class AUserListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = UserDataSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = UserListFilter
    search_fields = ['username', 'email', 'lastName', 'firstName']
    pagination_class = PaginationUser

    def get_queryset(self):
        UserList_object = User.objects.order_by('id').filter(is_active=True)
        return UserList_object