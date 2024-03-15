from django.urls import path
from . import views


urlpatterns = [
    path('info/', views.InfoView.as_view(), name="info"),
    path('user_data/', views.UserDataView.as_view(), name='user_data'),
    path('my_courses/', views.MyCoursesView.as_view(), name="my_courses"),
    path('my_courses/my_course_details/<int:pk>/', views.MyCourseDetailsView.as_view(), name="my_course_details"),

    #Admin users
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/edit_user/<int:pk>/', views.EditUserView.as_view(), name='edit_user'),
    path('users/delete_user/<int:pk>/', views.DeleteUserView.as_view(), name='delete_user'),

    #Admin courses
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('courses/add_course/', views.AddCourseView.as_view(), name='add_course'),
    path('courses/edit_course/<int:pk>/', views.EditCourseView.as_view(), name='edit_course'),
    path('courses/delete_course/<int:pk>/', views.DeleteCourseView.as_view(), name='delete_course'),

    #Admin sessions
    path('courses/add_session/', views.AddSessionView.as_view(), name='add_session'),
    path('courses/edit_session/<int:pk>/', views.EditSessionView.as_view(), name='edit_session'),
    path('courses/delete_session/<int:pk>/', views.DeleteSessionView.as_view(), name='delete_session'),
]
