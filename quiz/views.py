from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Quizzes, Category, Question
from .serializers import QuizSerializer, CategorySerializer, RandomQuestionSerializer


class Quiz(generics.ListCreateAPIView):
    serializer_class = QuizSerializer
    queryset = Quizzes.objects.all()   


class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuizSerializer
    queryset = Quizzes.objects.all()
    lookup_field = 'id'


class Category(generics.CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    
class RandomQuestion(APIView):
    def get(self, request, format=None, **kwargs):
        question = Question.objects.filter(quiz__title=kwargs.get('topic')).order_by('?')[:1]
        print(Question.objects.filter(quiz__title=kwargs.get('topic')).order_by('?').query)
        serializer = RandomQuestionSerializer(question, many=True)
        return Response(serializer.data)