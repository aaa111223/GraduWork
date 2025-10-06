from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.AdminUserManagementViewSet, basename='admin_users')
router.register(r'jobs', views.AdminJobManagementViewSet, basename='admin_jobs')
router.register(r'feedbacks', views.AdminFeedbackManagementViewSet, basename='admin_feedbacks')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/stats/', views.AdminDashboardStatsView.as_view(), name='admin_dashboard_stats'),
    path('system/settings/', views.AdminSystemSettingsView.as_view(), name='admin_system_settings'),
]
