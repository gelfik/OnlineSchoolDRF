from rest_framework import serializers

from CoursesApp.models import CoursesListModel, CoursesSubCoursesModel
from CoursesApp.serializers import CoursesSubCoursesSerializer
from LessonApp.models import LessonModel
from LessonApp.serializers import LessonAPanelSerializer, LessonAPanelDetailSerializer
from UserProfileApp.serializers import UserMentorSerializer


class ACoursesCoursesDetailSerializer(serializers.ModelSerializer):
    # teacher = TeacherDataForPurchaseSerializer(many=False, read_only=True)
    mentors = UserMentorSerializer(many=True, read_only=True)
    predmet = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    courseExamType = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # subCourses = CoursesSubCoursesSerializer(read_only=True, many=True)
    subCourses = serializers.SerializerMethodField(read_only=True, source='get_subCourses')

    # purchaseList = PurchaseListForAPanelCoursesSerializer(read_only=True, many=True)

    class Meta:
        model = CoursesListModel
        # fields = '__all__'
        # fields = ('name', 'predmet', 'courseType', 'courseExamType', 'coursePicture', 'mentors',)
        exclude = ('teacher', 'is_active',)

    def get_subCourses(self, instance):
        return CoursesSubCoursesSerializer(many=True, instance=instance.subCourses.filter(is_active=True),
                                                      context={'request': self.context['request']}).data

# class APanelCoursesEditSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CoursesListModel
#         fields = (
#             'name', 'shortDescription', 'description', 'price', 'discountDuration', 'buyAllSubCourses', 'draft',
#             'predmet', 'courseType', 'courseExamType',)

    # def update(self, instance, validated_data):
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()
    #     return instance


class ACoursesSubCoursesDetailSerializer(serializers.ModelSerializer):
    # lessons = LessonListForAPanelSerializer(many=True, read_only=True)
    lessons = serializers.SerializerMethodField(read_only=True, source='get_lessons')

    class Meta:
        model = CoursesSubCoursesModel
        exclude = ('is_active',)

    def get_lessons(self, instance):
        return LessonAPanelSerializer(many=True, instance=instance.lessons.filter(is_active=True),
                                                      context={'request': self.context['request']}).data


class ACoursesLessonDetailSerializer(serializers.ModelSerializer):
    lessons = LessonAPanelDetailSerializer(many=True, read_only=True)

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
