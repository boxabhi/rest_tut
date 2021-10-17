
from home.models import Student
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.decorators import action



class DepartmentMixin:
    
    @action(detail=False, methods=['GET'])
    def get_department_detail(self , request , pk=None):
        try:
            department_obj = Department.objects.all()
            serializer = DepartmentSerializer(department_obj , many= True)
            return Response({
                'status' : True,
                'message' : 'department fetched ',
                'data'  : serializer.data
            })

        except Exception as e:
            print(e)
            return Response({
            'status' : False,
            'message' : 'invali uid',
            'data' : {}
        })

        
    @action(detail=False, methods=['POST'])
    def assign_department_to_student(self, request, pk=None):
        data = request.data
        serializer = DepartmentValidationSerializer(data = data)
        if serializer.is_valid():
            student_uid = serializer.data['student_uid']
            department_uid = serializer.data['department_uid']
            student_obj = Student.objects.filter(uid = student_uid , department__isnull = True).first()
            department_obj = Department.objects.filter(uid = department_uid).first()

            if student_obj is None:
                return Response({
                        'status' : False,
                        'message' : 'invalid student uid or department is already assigned',
                        'data' : {}
                    })

            
            if  department_obj is None:
                return Response({
                        'status' : False,
                        'message' : 'invalid department uid',
                        'data' : {}
                    })  
            
            student_obj.department = department_obj
            student_obj.save()

            return Response({
            'status' : True,
            'message' : 'department assigned successfully',
            'data' : {}
            })

        return Response({
            'status' : False,
            'message' : 'error',
            'data' : serializer.errors
        })



             