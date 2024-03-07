from django.urls import path
from . import views


urlpatterns = [
    path('info/', views.info, name="info"),
    path('user_data/', views.user_data, name='user_data'),
    path('my_courses/', views.my_courses, name="my_courses"),
    path('my_courses/my_course_details/<int:pk>/', views.my_course_details, name="my_course_details"),

    #Admin users
    path('users/', views.users, name='users'),
    path('users/edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path('users/delete_user/<int:pk>/', views.delete_user, name='delete_user'),

    #Admin courses
    path('courses/', views.courses, name='courses'),
    path('courses/add_course/', views.add_course, name='add_course'),
    path('courses/edit_course/<int:pk>/', views.edit_course, name='edit_course'),
    path('courses/delete_course/<int:pk>/', views.delete_course, name='delete_course'),

    #Admin sessions
    path('courses/add_session/', views.add_session, name='add_session'),
    path('courses/edit_session/<int:pk>/', views.edit_session, name='edit_session'),
    path('courses/delete_session/<int:pk>/', views.delete_session, name='delete_session'),
]
