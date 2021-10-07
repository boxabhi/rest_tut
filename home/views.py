from django.utils.translation import LANGUAGE_SESSION_KEY
from rest_framework.views import APIView
from home.serializer import RegistrationSerializer, StudentSerializer,PasswordSerializer , DepartmentSerializer
from home.models import Student
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
# Create a model which has foreging key and many to many relationship. Now add some dummy data using faker library. Create a serializer which serialize all the fields including foreign key and many to many.S -

# CRUD
# @api_view('create-stuen) 
# @api_view('delete-)
# @api_view('pac)
# @api_view('pucy)
# Django rest framework

from rest_framework import status, viewsets
from .models import *

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def list(self, request):
        objs = Department.objects.all()
        if request.GET.get('uid'):
            objs = objs.filter(uid = request.GET.get('uid'))
        serializer = DepartmentSerializer(objs , many= True)
        return Response({
            'status' : 200,
            'message' : 'data',
            'data' : serializer.data
        })
        


class DemoAPI(APIView):

    def get(self , request):
        objs = Department.objects.all()

        if request.GET.get('type'):
            if request.GET.get('type') == 'exclude':
                objs = objs.exclude(uid = request.GET.get('uid'))

        if request.GET.get('uid'):
            objs = objs.exclude(uid = request.GET.get('uid'))
        
            
        serializer = DepartmentSerializer(objs , many= True)
        return Response({
            'status' : 200,
            'message' : 'data',
            'data' : serializer.data
        })

    def post(self , request):
        data = request.data

        serializer = DepartmentSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status' : True , 
                'data' : serializer.data
            })

        return Response({
            'status' : False,
            'message' : serializer.errors
        })

    def put(self , request):
        data = request.data
        try:
            obj = Department.objects.get(uid = data.get('uid'))
        except Exception as e:
            return Response({
                'status' : False,
                'message' : 'object does not exists' 
            })
        serializer = DepartmentSerializer(obj, data)

        if serializer.is_valid():
            serializer.save()
            return Response({
            'status' : 200,
            'message' : 'data',
            'data' : serializer.data
            })
        return Response({
            'status' : False,
            'message' : serializer.errors
        })
    
    
    def patch(self , request):
        data = request.data
        obj = Department.objects.get(uid = data.get('uid'))
        serializer = DepartmentSerializer(obj, data , partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response({
            'status' : 200,
            'message' : 'data',
            'data' : serializer.data
            })
        return Response({
            'status' : False,
            'message' : serializer.errors
        })

    
        return Response({
            'status' : True,
            'message' : 'PATCH API'
        })

    def delete(self , request):
        data = request.data
        try:
            obj = Department.objects.get(uid = data.get('uid')).delete()
            return Response({
                'status' : True,
                'message' : 'object delete' 
            })
        except Exception as e:
            return Response({
                'status' : False,
                'message' : 'object does not exists' 
            })
        return Response({
            'status' : True,
            'message' : 'DELET API'
        })

class RegistrationView(APIView):
    def get(self , request):
        pass
    def post(self , request):
        try:
            data = request.data
            serializer = RegistrationSerializer(data = data)
            if serializer.is_valid():
                username = serializer.data['username']
                email = serializer.data['email']
                password = serializer.data['password']

                if User.objects.filter(email = email).exists():
                    return Response({
                        'status' :False,
                        'message' : 'email is taken',
                        'data' : {}
                    })
                
                if User.objects.filter(username = username).exists():
                    return Response({
                        'status' :False,
                        'message' : 'username is taken',
                        'data' : {}
                    })

                user_obj = User.objects.create(
                    username = username , 
                    email = email
                )
                user_obj.set_password(password)

                return Response({
                    'status' : 200,
                    'message' : 'user created',
                    'data' : {}
                })

            return Response({
                'status' :False,
                'message' : 'invalid keys',
                'data' : serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status' : 400,
                'message' : 'something went wrong',
                'data' : {}
            })


from .serializer import *

class LoginView(APIView):
    def post(self , request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                username = serializer.data['username']
                password = serializer.data['password']
                if not User.objects.filter(username = username).exists():
                    return Response({
                        'status' :False,
                        'message' : 'user not found',
                        'data' : {}
                    })
                
                user_obj = authenticate(username = username , password = password)

                if user_obj is None:
                    return Response({
                        'status' :False,
                        'message' : 'invalid password',
                        'data' : {}
                    })

                token , _ = Token.objects.get_or_create(user = user_obj)
                return Response({
                        'status' :True,
                        'message' : 'login success',
                        'data' : {
                            'token' : str(token)
                        }
                    })
                
        
        except Exception as e:
            print(e)
            return Response({
                'status' : 400,
                'message' : 'something went wrong',
                'data' : {}
            })
            


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class StudentView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        print(request.user)
        objs = Student.objects.filter(department__isnull = False)
        serializer = StudentSerializer(objs , many= True)
        return Response({
            'status' : 200,
            'message' : 'data',
            'data' : serializer.data
        })


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