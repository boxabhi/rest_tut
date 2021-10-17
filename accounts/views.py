from re import I
from django.shortcuts import render
from rest_framework.views import APIView
from home.serializer import RegistrationSerializer, StudentSerializer,PasswordSerializer , DepartmentSerializer,DepartmentValidationSerializer
from home.models import Student
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *




class RegisterView(APIView):
    def post(self , request):
        try:
            data = request.data
            serializer = UserSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : 200,
                    'message' : 'data',
                    'data' : serializer.data
                })

            return Response({
            'status' : False,
            'message' : 'error',
            'data' : serializer.errors
            })
        except Exception as e:
            print(e)

            return Response({
                    'status' : False,
                    'message' : 'error',
                    'data' : {}
                })
    
    def patch(self , request):
        try:
            data = request.data
            obj = User.objects.get(id = data['id'])
            serializer = UserSerializer(obj,data = data , partial = True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : 200,
                    'message' : 'data',
                    'data' : serializer.data
                })

            return Response({
            'status' : False,
            'message' : 'error',
            'data' : serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                    'status' : False,
                    'message' : 'error',
                    'data' : {}
                })


            


class VeriyOTP(APIView):
    def post(self , request):
        data = request.data

        profile_obj = Profile.objects.get(user__username = data.get('username'))

        if profile_obj.token == data.get('otp'):
            profile_obj.is_active = True
            profile_obj.save()
            return Response({
            'status' : False,
            'message' : 'correct OTP',
            'data' :{}
            })
        return Response({
            'status' : False,
            'message' : 'wrong OTP',
            'data' :{}
            })



            
from django.http import HttpResponse


def verify_email(request , token):
    obj = Profile.objects.filter(token = token)

    if obj.exists():
        obj = obj[0]
        obj.is_active = True
        obj.save()
        return HttpResponse('Your account activated')
    
    return HttpResponse('Invalid token')
    
