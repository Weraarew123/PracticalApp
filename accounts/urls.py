from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),

    path('forgotPassword/', views.ForgotPasswordView.as_view(), name='forgotPassword'),
    #path("forgotPassword/", auth_views.PasswordResetView.as_view(template_name="accounts/forgotPassword.html", email_template_name="accounts/reset_password_email.html"), name="forgotPassword"),
    path('password_reset_confirm/<uidb64>/<token>/', views.ResetPasswordValidateView.as_view(), name='password_reset_confirm'),
    #path("resetPassword_validate/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('resetPassword/', views.ResetPasswordView.as_view(), name='resetPassword'),
    #path("resetPassword/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/resetPassword.html"), name="password_reset_confirm"),
    #path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('change_email/', views.ChangeEmailView.as_view(), name='change_email'),
    path('change_email/new_email', views.NewEmailView.as_view(), name='new_email'),
    path('change_email_validation/<uidb64>/<token>/<email>/', views.ChangeEmailValidationView.as_view(), name='change_email_validation'),
]