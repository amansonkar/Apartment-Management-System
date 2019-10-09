from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', auth_views.LoginView.as_view(template_name= 'accounts/signin.html'), name='signin'),
    path('login/', views.loginView,name='login'),
    path('signout/', auth_views.LogoutView.as_view(template_name= 'accounts/signout.html'), name='signout'),
    path('signup/', views.signup, name='signup'),
    path('register/',views.regView,name='register'),
    path('user/', views.user_home,name='user_home'),
    path('user/profile/', views.view_profile, name='view_profile'),
    path('user/profile/edit/', views.edit_profile, name='edit_profile'),
    path('user/change-password/', views.change_password, name='change_password'),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/users/reset/done/'), name='reset_password_confirm'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view()),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view()),
    path('generate/',views.generate_otp,name='generate'),
    path('validate/',views.validate_otp,name='validate'),
    path('verify/',views.verify_otp,name='verify'),
]