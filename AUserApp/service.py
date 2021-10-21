from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from django.core.paginator import Paginator
from django.utils.functional import cached_property

from urllib import parse
from django.utils.encoding import force_str
from django.contrib.auth.models import Group
from UserProfileApp.models import User

class PaginationUser(PageNumberPagination):
    page_size = 1
    max_page_size = 1000

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        (scheme, netloc, path, query, fragment) = parse.urlsplit(force_str(self.request.build_absolute_uri()))
        return replace_query_param(f'?{query}', self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        (scheme, netloc, path, query, fragment) = parse.urlsplit(force_str(self.request.build_absolute_uri()))
        return replace_query_param(f'?{query}', self.page_query_param, page_number)

    def get_paginated_response(self, data):
        # print(self.page.paginator.num_pages)
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'curent': self.page.number,
            'count': self.page.paginator.num_pages,
            'countItem': self.page.paginator.count,
            'results': data
        })


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class UserListFilter(filters.FilterSet):
    # predmet = CharFilterInFilter(field_name='predmet__name', lookup_expr='in')
    # exam = CharFilterInFilter(field_name='courseExamType__name', lookup_expr='in')
    # type = CharFilterInFilter(field_name='courseType__name', lookup_expr='in')
    # role = filters.BooleanFilter(field_name='groups__name')
    # role = CharFilterInFilter(field_name='groups__name')
    role = CharFilterInFilter(field_name='groups__name', method='filter_role')

    class Meta:
        model = User
        fields = ['role', ]

    def filter_role(self, queryset, name, role):
        try:
            Group.objects.get(name=role[0])
            return queryset.filter(groups__name=role[0])
        except Group.DoesNotExist:
            return queryset