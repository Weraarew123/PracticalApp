from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword_validate/<uidb64>/<token>/', views.resetPassword_validate, name='resetPassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

    path('change_email/', views.change_email, name='change_email'),
    path('change_email/new_email', views.new_email, name='new_email'),
    path('change_email_validation/<uidb64>/<token>/<email>/', views.change_email_validation, name='change_email_validation'),
]