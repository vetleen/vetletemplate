from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('change-password/', views.change_password, name='change-password'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-up-complete/', views.sign_up_complete, name='sign-up-complete'),
]
