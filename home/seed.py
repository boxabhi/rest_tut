from .models import Student
from faker import Faker
fake = Faker()
import random


choice = ['Male' , 'Female']

def seed_db(n):
    for i in range(0 , n):
        Student.objects.create(
            student_name = fake.name(),
            student_age =  random.randint(18 , 40),
            student_address  = fake.address(),
            student_gender = random.randint(0 , 1)
        )