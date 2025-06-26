from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
    
    path('login', views.login_view, name="login"),
    path('register', views.register_view, name="register"),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    
     path('password-reset/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_link_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_change.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    
]