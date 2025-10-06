from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.JobApplicationViewSet, basename='job_application')
router.register(r'interviews', views.InterviewViewSet, basename='interview')

urlpatterns = [
    path('', include(router.urls)),
    path('my-applications/', views.MyApplicationsView.as_view(), name='my_applications'),
    path('enterprise-applications/', views.EnterpriseApplicationsView.as_view(), name='enterprise_applications'),
    path('<int:application_id>/status/', views.UpdateApplicationStatusView.as_view(), name='update_status'),
    path('<int:application_id>/schedule-interview/', views.ScheduleInterviewView.as_view(), name='schedule_interview'),
    path('statistics/', views.ApplicationStatisticsView.as_view(), name='application_statistics'),
]
