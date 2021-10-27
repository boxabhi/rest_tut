
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import  viewsets

from quiz.serializers import QuizQuestionsSerializer, QuizSerializer , CheckQuestionSerializer
from .models import *
from rest_framework.decorators import action


class QuizView(APIView):

    def get(self , request):
        try:
            quiz_name = request.GET.get('quiz_name')
            if not quiz_name:
                return Response({
                'status' : False,
                'message' :'quiz name is required',
                'data' : {}
            })
            
            quiz_obj = Quiz.objects.filter(quiz_name__icontains= request.GET.get('quiz_name'))
            if not quiz_obj.exists():
                return Response({
                    'status' : False,
                    'message' :'no quiz found',
                    'data' : {}
                })
            quiz_questions = quiz_obj[0].quiz_questions.all()
            serializer = QuizQuestionsSerializer(quiz_questions , many = True)

            return Response({
                'status' : True,
                'message' :'your quiz',
                'data' : serializer.data
            })
        
        except Exception as e:
            print(e)

            return Response({
                'status' : False,
                'message' :'somethign went wrong',
                'data' : {}
            })



    def post(self , request):
        try:
            data = request.data
            serializer = QuizSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                quiz_obj = Quiz.objects.get(uid = serializer.data['uid'])
                questions_objs = Question.objects.filter(
                    category = quiz_obj.category)[0:quiz_obj.question_limit]

                for questions_obj in questions_objs:
                    QuizQuestions.objects.create(
                     quiz = quiz_obj,
                     question = questions_obj
                    )
                return Response({
                    'status' : True,
                    'message' : 'Your quiz has been created',
                    'data' : {}
                })
            return Response({
                    'status' : False,
                    'message' : 'you have some errors',
                    'data' : serializer.errors
                })
            

                
        except Exception as e:
            print(e)
            return Response({
                'status' : False,
                'message' :'somethign went wrong',
                'data' : {}
            })



class CheckQuestion(APIView):
    def post(self , request):
        try:
            data = request.data

            serializer = CheckQuestionSerializer(data = data)
            if serializer.is_valid():
                answer = serializer.data['answer']
                question = serializer.data['question']
                question_obj = Question.objects.get(uid = question)

                if not question_obj.answer.filter(answer = answer).exists():
                    return Response({
                        'status' : False , 
                        'message' : 'it seems option is not present',
                        'data' : {}
                    })


                if question_obj.answer.filter(answer = answer , is_correct = True).exists():
                    return Response({
                        'status' : True , 
                        'message' : 'Hurray your answer is correct',
                        'data' : {}
                    })
                
                return Response({
                        'status' : False , 
                        'message' : 'no your answer is in-correct',
                        'data' : {}
                    })
            return Response({
                        'status' : False , 
                        'message' : 'somethign went error',
                        'data' : serializer.errors
                    })
        except Exception as e:
            return Response({
                        'status' : False , 
                        'message' : 'no your answer is in correct',
                        'data' : {}
                    })

