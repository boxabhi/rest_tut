from django.db.models import fields
from rest_framework import serializers
from rest_framework.views import exception_handler
from .models import *

class QuestionSerializer(serializers.ModelSerializer):
    answers  = serializers.SerializerMethodField()
    class Meta:
        model = Question
        exclude = ['created_at' , 'updated_at' , 'category']
    
    def get_answers(self , obj):
        serializer = AnswerSerializer(obj.answer.all() , many = True)
        return serializer.data


class AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answer
        exclude = ['created_at' , 'updated_at' , 'uid' , 'is_correct' , 'question']




class QuizSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Quiz
        exclude = ['created_at' , 'updated_at']


class QuizQuestionsSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    class Meta:
        model = QuizQuestions
        exclude = ['created_at' , 'updated_at' , 'uid' , 'quiz']


    def get_questions(self , obj):
        serializer = QuestionSerializer(obj.question)
        return serializer.data



class CheckQuestionSerializer(serializers.Serializer):
    answer = serializers.CharField()
    question = serializers.UUIDField()
    