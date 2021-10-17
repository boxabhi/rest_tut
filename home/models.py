from django.db import models
import uuid

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4 , primary_key=True , editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Department(BaseModel):

    department_name = models.CharField(max_length=100)
    s_no = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "school_department"




class Student(BaseModel):
    department = models.ForeignKey(Department ,null=True , blank=True, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_age = models.IntegerField()
    student_address = models.CharField(max_length=100)
    student_gender = models.CharField(max_length=10 , choices = (('Male' , 'Male') , ('Female' , 'Female')))
    #departments = models.ManyToManyField(Department)
    def __str__(self) -> str:
        return self.student_name
