from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [
    path('authenticate/', obtain_jwt_token),
    path('refresh/', refresh_jwt_token), 
    path('verify/', verify_jwt_token),
]
