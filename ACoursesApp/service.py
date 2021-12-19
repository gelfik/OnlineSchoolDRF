from django_filters import rest_framework as filters

from CoursesApp.models import CoursesListModel
from PurchaseApp.models import PurchaseListModel


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CoursesListFilter(filters.FilterSet):
    predmet = CharFilterInFilter(field_name='predmet__name', lookup_expr='in')
    exam = CharFilterInFilter(field_name='courseExamType__name', lookup_expr='in')
    type = CharFilterInFilter(field_name='courseType__name', lookup_expr='in')
    draft = filters.BooleanFilter(field_name='draft')

    class Meta:
        model = CoursesListModel
        fields = ['predmet', 'exam', 'type', 'draft', ]


class CoursesPurchaseFilter(filters.FilterSet):
    courseSub = CharFilterInFilter(field_name='pay__courseSub__id', lookup_expr='in')

    class Meta:
        model = PurchaseListModel
        fields = ['courseSub', ]