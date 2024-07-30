"""application admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from . import views
from .views import *

urlpatterns = [
    # Admin
    path('admin/user/add', CreateUserView.as_view(), name='admin-user-add'),
    path('admin/user/', ListUserView.as_view(), name='admin-user-list'),
    path('admin/user/list/ajax', ListUserViewJson.as_view(), name='admin-user-list-ajax'),
    path('admin/user/detail/<int:pk>', DetailUserView.as_view(), name='admin-user-detail'),
    path('admin/user/edit/<int:pk>', UpdateUserView.as_view(), name='admin-user-edit'),
    path('admin/user/delete/<int:pk>', DeleteUserView.as_view(), name='admin-user-delete'),

    # Frontend User
    path('', LandingView.as_view(), name="landing"),
    path('login/', LoginView.as_view(), name="user-login"),
    # path('register/', RegisterView.as_view(), name="user-register"),
    path('logout/', LogoutView.as_view(), name="user-logout"),
    path('profile/', UpdateUserProfileView.as_view(), name="user-profile"),
    path('change-password/', ChangeUserSelfPasswordView.as_view(), name="user-change-password"),
    path('home/', HomePageView.as_view(), name="user-home"),
    path('user/service/list/ajax', ListServiceUserViewJson.as_view(), name='user-service-list-ajax'),
    path('buy/service/<int:pk>', BuyServiceView.as_view(), name='buy-service'),

    path('subscribe/<int:service_id>/', views.subscribe_service, name='subscribe-service'),
    path('razorpay/callback/', views.razorpay_callback, name='razorpay_callback'),
    path('subscription/success/', views.subscription_success, name='subscription_success'),
    # email
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('otp-confirmation/', OTPConfirmationView.as_view(), name='otp-confirmation'),
]
