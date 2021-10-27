from django.contrib import admin
from django.urls import path
from .views import *





urlpatterns = [
    path('create-quiz/' , QuizView.as_view()),
    path('check/' , CheckQuestion.as_view())
]


