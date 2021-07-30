from rest_framework import serializers
from .models import CoursesNameModel, CoursesPredmetModel, CoursesExamTypeModel, CoursesListModel
from TeachersApp.serializers import TeacherDataSerializer


class CoursesExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesExamTypeModel
        fields = ('name',)


class CoursesPredmetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesPredmetModel
        fields = ('name',)


class CoursesNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesNameModel
        fields = ('name',)


class CoursesListSerializer(serializers.ModelSerializer):
    predmet = CoursesPredmetSerializer(many=False, read_only=True)
    courseName = CoursesNameSerializer(many=False, read_only=True)
    courseExamType = CoursesExamTypeSerializer(many=False, read_only=True)
    teacher = TeacherDataSerializer(many=False, read_only=True)

    class Meta:
        model = CoursesListModel
        fields = ('predmet', 'courseName', 'courseExamType', 'teacher', 'price',)

    def to_representation(self, instance):
        teacher = TeacherDataSerializer(instance=instance.teacher, many=False, read_only=True,
                                        context={'request': self.context['request']})
        return {'id': instance.id,
                'predmet': instance.predmet.name,
                'courseName': instance.courseName.name,
                'courseExamType': instance.courseExamType.name,
                'teacher': teacher.data,
                'price': instance.price,
                }


class FilterDataSerializer(serializers.Serializer):
    predmet = CoursesPredmetSerializer(many=True, read_only=True)
    courseName = CoursesNameSerializer(many=True, read_only=True)
    examType = CoursesExamTypeSerializer(many=True, read_only=True)

    class Meta:
        fields = ('predmet', 'courseName', 'examType',)

    def to_representation(self, instance):
        predmet = CoursesPredmetSerializer(instance=instance['predmet'], many=True)
        courseName = CoursesNameSerializer(instance=instance['courseName'], many=True)
        examType = CoursesExamTypeSerializer(instance=instance['examType'], many=True)
        return {'predmet': predmet.data,
                'courseName': courseName.data,
                'examType': examType.data,
                }
