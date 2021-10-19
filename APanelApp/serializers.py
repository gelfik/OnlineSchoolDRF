from rest_framework import serializers

from CoursesApp.models import CoursesListModel, CoursesSubCoursesModel
from CoursesApp.serializers import CoursesSubCoursesSerializer
from HomeworkApp.serializers import HomeworkListDetailSerializer
from LessonApp.models import LessonModel
from LessonApp.serializers import LessonListForAPanelSerializer, LessonVideoSerializer, LessonFileListSerializer
from UserProfileApp.serializers import UserMentorSerializer


class APanelCoursesDetailSerializer(serializers.ModelSerializer):
    # teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    mentors = UserMentorSerializer(many=True, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    subCourses = CoursesSubCoursesSerializer(read_only=True, many=True)

    # purchaseList = PurchaseListForAPanelCoursesSerializer(read_only=True, many=True)

    class Meta:
        model = CoursesListModel
        # fields = '__all__'
        # fields = ('name', 'predmet', 'courseType', 'courseExamType', 'coursePicture', 'mentors',)
        exclude = ('teacher', 'is_active',)


class APanelCoursesEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoursesListModel
        fields = (
        'name', 'shortDescription', 'description', 'price', 'discountDuration', 'buyAllSubCourses', 'draft', 'predmet',
        'courseType', 'courseExamType',)

    # def update(self, instance, validated_data):
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()
    #     return instance


class APanelSubCoursesDetailSerializer(serializers.ModelSerializer):
    lessons = LessonListForAPanelSerializer(many=True, read_only=True)

    class Meta:
        model = CoursesSubCoursesModel
        exclude = ('is_active',)


class APanelLessonDetailSerializer(serializers.ModelSerializer):
    homework = HomeworkListDetailSerializer(many=False, read_only=True)
    video = LessonVideoSerializer(many=False, read_only=True)
    files = LessonFileListSerializer(many=False, read_only=True)

    class Meta:
        model = LessonModel
        exclude = ('is_active',)

# class APanelCoursesDetailSerializer(serializers.ModelSerializer):
#     # teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
#     mentors = UserMentorSerializer(many=True, read_only=True)
#     predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
#     courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
#     courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)
#     subCourses = CoursesSubCoursesSerializer(read_only=True, many=True)
#     # purchaseList = PurchaseListForAPanelCoursesSerializer(read_only=True, many=True)
#     purchaseList = serializers.SerializerMethodField(read_only=True, source='get_purchaseList')
#
#     class Meta:
#         model = CoursesListModel
#         # fields = '__all__'
#         # fields = ('name', 'predmet', 'courseType', 'courseExamType', 'coursePicture', 'mentors',)
#         exclude = ('teacher', 'is_active',)
#
#     def get_purchaseList(self, instance):
#         purchaseList = PurchaseListModel.objects.filter(course=instance.id)
#         return PurchaseListForAPanelCoursesSerializer(read_only=True, many=True, instance=purchaseList,
#                                                       context={'request': self.context['request']}).data
