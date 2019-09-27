from django.urls import path
from . import views

urlpatterns = [
    path('registeruser/signup/', views.SignUp.as_view(), name='signup'),
    path('<int:pk>/update', views.CustomUserUpdate.as_view(), name='edit-user'),
]
