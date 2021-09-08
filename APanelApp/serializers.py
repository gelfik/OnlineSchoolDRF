from rest_framework import serializers

from CoursesApp.models import CoursesSubCoursesModel, CoursesListModel
from CoursesApp.serializers import CoursesDetailForPurchaseSerializer, CoursesSubCoursesSerializer, \
    CoursesForPurchaseSerializer, CoursesDetail, CoursesListSerializer, CoursesForPurchaseListSerializer, \
    CoursesForCourseSerializer
from HomeworkApp.models import HomeworkListModel
from HomeworkApp.serializers import HomeworkAskSerializer, HomeworkAskAnswerSelectionOnListAnswersSerializer, \
    HomeworkListDetailSerializer, HomeworkAskAnswersSerializer
from LessonApp.models import LessonModel, LessonListModel
from LessonApp.serializers import LessonVideoSerializer, LessonFileListSerializer, LessonVideoForListSerializer, \
    LessonFilesForListSerializer



class PurchasePaySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(read_only=True, source='get_date')

    class Meta:
        model = CoursesListModel
        # fields = '__all__'
        fields = ('date', 'sumPay',)
        # exclude = ('draft', 'is_active',)

    def get_date(self, obj):
        return obj.date.strftime('%d.%m.%Y %H:%M')

