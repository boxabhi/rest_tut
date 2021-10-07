from rest_framework import serializers
from rest_framework.views import exception_handler
from .models import *



class RegistrationSerializer(serializers.Serializer):
    username   = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    username   = serializers.CharField()
    password = serializers.CharField()




class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    #lsconfirm_password = serializers.CharField()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ['created_at' , 'updated_at']

    def has_numbers(self , text):
        return any(t.isdigit() for t in text)

    def validate(self, validated_data):
        
        if 'department_name' in validated_data:
            if self.has_numbers(validated_data['department_name']):
                raise serializers.ValidationError("department_name connot be number")

        if 's_no' in validated_data:
            if validated_data['s_no'] < 0:
                raise serializers.ValidationError("number cannot be negative")

        return validated_data


class StudentSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    class Meta:
        model = Student
        exclude = ['created_at' , 'updated_at']
        depth = 1
    
    def get_department(self , obj):
        #[1 , 2, ,3 ]
        
        serializer = DepartmentSerializer(obj.department.all() , many = True)
        return serializer.data