from home.serializer import StudentSerializer
from home.models import Student
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def home(request):

    objs = Student.objects.all()
    serializer = StudentSerializer(objs , many= True)

    return Response({
        'status' : 200,
        'message' : 'data',
        'data' : serializer.data
    })
