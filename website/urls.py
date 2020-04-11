from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('change-password/', views.change_password, name='change-password'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('login/', views.login_view, name='loginc'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-account/', views.edit_account_view, name='edit-account'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

]
