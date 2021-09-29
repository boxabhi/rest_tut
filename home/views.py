from rest_framework import serializers
from rest_framework.views import exception_handler
from home.serializer import StudentSerializer,PasswordSerializer
from home.models import Student
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create a model which has foreging key and many to many relationship. Now add some dummy data using faker library. Create a serializer which serialize all the fields including foreign key and many to many.

@api_view()
def home(request):
    objs = Student.objects.filter(department__isnull = False)
    serializer = StudentSerializer(objs , many= True)
    return Response({
        'status' : 200,
        'message' : 'data',
        'data' : serializer.data
    })

@api_view(['POST'])
def store_student(request):
    try:
        data = request.data
        serializer = StudentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status' : 200,
                'message' : 'student created',
                'data' : serializer.data
            })
        return Response({
                'status' : 400,
                'message' : 'student not created',
                'data' : serializer.errors
        })
    except Exception as e:
        print(e)
        return Response({
                'status' : 400,
                'message' : 'something went wrong',
                'data' : {}
        })


@api_view(['POST'])
def change_password(request):
    try:
        data = request.data
        serializer = PasswordSerializer(data = data)
        if serializer.is_valid():
            old_password = serializer.data['old_password']
            new_password = serializer.data['new_password']
            print(old_password)
            return Response({
                'status' : 200,
                'message' : 'student created',
                'data' : serializer.data
            })
        
        return Response({
                'status' : 400,
                'message' : 'error',
                'data' : serializer.errors
        })

    except Exception as e:
        print(e)
        return Response({
                'status' : 400,
                'message' : 'something went wrong',
                'data' : {}
        })








#change-password => 'old_password' , 'new_password'