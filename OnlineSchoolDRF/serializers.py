from django.db.models import Avg, Count, Q
from rest_framework import serializers

from LessonApp.models import LessonResultUserModel
from OnlineSchoolDRF.service import int_r
from ProgressApp.serializers import ProgressResultSerializer


class UserProgressSerializer(serializers.Serializer):
    userProgress = serializers.SerializerMethodField(read_only=True, source='get_userProgress')

    def get_userProgress(self, instance):
        model_name = instance._meta.model.__name__
        results = LessonResultUserModel.objects.exclude(
            Q(taskABC__result=None) | Q(testCHL__result=None) | Q(testPOL__result=None)).filter(
            user=self.context['request'].user, is_active=True)
        if model_name == 'PurchaseListModel':
            results = results.filter(lessonmodel__lessons__courseslistmodel=instance.course.id)
        elif model_name == 'CoursesSubCoursesModel':
            results = results.filter(lessonmodel__lessons__purchasepaymodel__courseSub=instance.id)
        elif model_name == 'LessonModel':
            results = results.filter(lessonmodel__lessons__purchasepaymodel__courseSub__lessons=instance.id)
        localDataAVG = results.distinct().aggregate(pol=Avg('testPOL__result'), chl=Avg('testCHL__result'),
                                                    abc=Avg('taskABC__result'), countWork=Count('user'))
        localDataAVG.update(pol=int_r(localDataAVG['pol']), chl=int_r(localDataAVG['chl']),
                            abc=int_r(localDataAVG['abc']), countWork=localDataAVG['countWork'])
        localDataAVG.update(k=int_r((localDataAVG['pol'] * localDataAVG['chl'] * localDataAVG['abc']) ** (1 / 3)))
        return ProgressResultSerializer(many=False, instance=localDataAVG,
                                        context={'request': self.context['request']}).data
