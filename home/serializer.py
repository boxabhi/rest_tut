from rest_framework import serializers
from rest_framework.views import exception_handler
from .models import *


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    #confirm_password = serializers.CharField()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ['created_at' , 'updated_at']


class StudentSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    class Meta:
        model = Student
        exclude = ['created_at' , 'updated_at']
        depth = 1
    
    def get_department(self , obj):
        serializer = DepartmentSerializer(obj.department)
        return serializer.data