from django_filters import rest_framework as filters

from CoursesApp.models import CoursesListModel


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class AProgressCoursesListFilter(filters.FilterSet):
    predmet = CharFilterInFilter(field_name='predmet__name', lookup_expr='in')
    exam = CharFilterInFilter(field_name='courseExamType__name', lookup_expr='in')
    type = CharFilterInFilter(field_name='courseType__name', lookup_expr='in')

    class Meta:
        model = CoursesListModel
        fields = ['predmet', 'exam', 'type', ]