from django.contrib import admin
from django.urls import path
from home.views import *

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'department', DepartmentViewSet, basename='department')





urlpatterns = [
    path('' , home, ),
    path('store_student/' , store_student),
    path('student/' , StudentView.as_view()),
    path('change_password/' , change_password),
    path('registration/' , RegistrationView.as_view()),
    path('login/' , LoginView.as_view()),
    path('demo/' , DemoAPI.as_view()),
]


urlpatterns += router.urls
