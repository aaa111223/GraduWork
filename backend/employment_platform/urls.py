"""
URL configuration for employment_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    """API health check endpoint"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Student Employment Platform API is running',
        'version': '1.0.0'
    })

def dashboard_stats(request):
    """Dashboard statistics endpoint"""
    from apps.users.models import User
    from apps.jobs.models import Job
    from apps.applications.models import JobApplication

    # 获取真实统计数据
    total_users = User.objects.count()
    total_jobs = Job.objects.filter(status='published').count()
    total_applications = JobApplication.objects.count()
    successful_placements = JobApplication.objects.filter(status='accepted').count()

    return JsonResponse({
        'totalUsers': total_users,
        'totalJobs': total_jobs,
        'totalApplications': total_applications,
        'successfulPlacements': successful_placements
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    path('api/stats/dashboard/', dashboard_stats, name='dashboard_stats'),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/jobs/', include('apps.jobs.urls')),
    path('api/applications/', include('apps.applications.urls')),
    path('api/feedback/', include('apps.feedback.urls')),
    path('api/admin/', include('apps.admin_management.urls')),
]

# ??????????????????????
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
