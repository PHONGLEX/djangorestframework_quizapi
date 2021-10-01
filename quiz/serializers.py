from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Quizzes, Category, Question


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Quizzes
        fields = ("title", "category", "category_id")

    def validate(self, attrs):
        category_id = attrs.get('category_id')

        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError("The category matching the id does not exist")

        return attrs

    def create(self, validated_data):
        return Quizzes.objects.create(title=validated_data['title'], category_id=validated_data['category_id'])


class RandomQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'answer']