from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    # JWT Token相关
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # 用户认证相关
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    
    # 验证码相关
    path('send-code/', views.SendVerificationCodeView.as_view(), name='send_code'),
    path('verify-code/', views.VerifyCodeView.as_view(), name='verify_code'),
    
    # 登录日志
    path('login-logs/', views.LoginLogListView.as_view(), name='login_logs'),
]
