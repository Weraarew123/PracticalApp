from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),

    path('forgotPassword/', views.ForgotPasswordView.as_view(), name='forgotPassword'),
    path('resetPassword_validate/<uidb64>/<token>/', views.ResetPasswordValidateView.as_view(), name='resetPassword_validate'),
    path('resetPassword/', views.ResetPasswordView.as_view(), name='resetPassword'),

    path('change_email/', views.ChangeEmailView.as_view(), name='change_email'),
    path('change_email/new_email', views.NewEmailView.as_view(), name='new_email'),
    path('change_email_validation/<uidb64>/<token>/<email>/', views.ChangeEmailValidationView.as_view(), name='change_email_validation'),
]