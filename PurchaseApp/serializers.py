from rest_framework import serializers

from CoursesApp.models import CoursesSubCoursesModel
from CoursesApp.serializers import CoursesDetailForPurchaseSerializer, CoursesSubCoursesSerializer, \
    CoursesForPurchaseSerializer, CoursesDetail, CoursesListSerializer
from .models import PurchasePayModel, PurchaseListModel


class PurchasePaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasePayModel
        # fields = '__all__'
        fields = ('date', 'sumPay',)
        # exclude = ('draft', 'is_active',)


class PurchasePayDetailSerializer(serializers.ModelSerializer):
    promocode = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = PurchasePayModel
        # fields = '__all__'
        # fields = ('date', 'sumPay', 'sumFull', 'promocode', 'payStatus')
        exclude = ('is_active',)


class PurchaseListSerializer(serializers.ModelSerializer):
    course = CoursesForPurchaseSerializer(many=False, read_only=True)
    subCourses = CoursesSubCoursesSerializer(many=True, read_only=True)
    purchasePay = PurchasePaySerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseListModel
        # fields = '__all__'
        # fields = ('predmet', 'courseType', 'courseExamType', 'teacher', 'price', 'leasonList',)
        exclude = ('user', 'is_active',)


class PurchaseDetailSerializer(serializers.ModelSerializer):
    course = CoursesDetailForPurchaseSerializer(many=False, read_only=True)
    # subCourses = CoursesSubCoursesSerializer(many=True, read_only=True)
    purchasePay = PurchasePaySerializer(many=True, read_only=True)
    courseSub = serializers.SerializerMethodField(read_only=True, source='get_courseSub')

    class Meta:
        model = PurchaseListModel
        # fields = '__all__'
        # fields = ('predmet', 'courseType', 'courseExamType', 'teacher', 'price', 'leasonList',)
        exclude = ('id', 'user', 'is_active',)


    def get_courseSub(self, obj):
        if obj.courseSubAll:
            return CoursesSubCoursesSerializer(instance=obj.course.subCourses, many=True, read_only=True)
        else:
            return CoursesSubCoursesSerializer(instance=obj.courseSub, many=True, read_only=True)


    # def to_representation(self, instance):
    #     super(PurchaseDetailSerializer, self).to_representation(instance)
    #     if instance.courseSubAll:
    #         courseSub = CoursesSubCoursesSerializer(instance=instance.course.subCourses, many=True, read_only=True)
    #         courseSub = subCourses.data
    #     else:
    #         courseSub = instance.courseSub
    #     course = CoursesDetailForPurchaseSerializer(instance=instance.course, many=False, read_only=True)
    #     purchasePay = PurchasePaySerializer(instance=instance.purchasePay,many=True, read_only=True)
    #     return {
    #         'course': course.data,
    #         'courseSub': courseSub,
    #         'purchasePay': purchasePay.data
    #     }
