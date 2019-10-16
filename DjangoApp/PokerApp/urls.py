from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('jwt_auth.urls')),
    path('api/users/', include('users.urls')),
    path('api/games/', include('poker_api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
