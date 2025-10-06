from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.JobCategoryViewSet, basename='job_category')
router.register(r'favorites', views.JobFavoriteViewSet, basename='job_favorite')
router.register(r'', views.JobViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.JobSearchView.as_view(), name='job_search'),
    path('recommendations/', views.JobRecommendationView.as_view(), name='job_recommendations'),
    path('<int:job_id>/favorite/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
]
