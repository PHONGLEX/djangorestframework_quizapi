from django.urls import path

from . import views


urlpatterns = [
    path('', views.Quiz.as_view(), name='quiz'),
    path('<int:id>/', views.QuizDetail.as_view(), name='quiz-detail'),
    path('category/', views.Category.as_view(), name='category'),
    path('r/<str:topic>/', views.RandomQuestion.as_view(), name='random')
]