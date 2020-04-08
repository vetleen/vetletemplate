from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('change-password/', views.change_password, name='change-password'),
    path('password-change-completed/', views.password_change_done, name='password_change_done'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-up-complete/', views.sign_up_complete, name='sign-up-complete'),
    path('login/', views.login_view, name='loginc'),
    path('login-complete/', views.login_complete, name='login-complete'),
    path('logout/', views.logout_view, name='logout'),

]
