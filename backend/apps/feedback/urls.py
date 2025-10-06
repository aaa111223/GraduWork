from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.FeedbackCategoryViewSet, basename='feedback_category')
router.register(r'', views.FeedbackViewSet, basename='feedback')
router.register(r'notifications', views.SystemNotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('my-feedbacks/', views.MyFeedbacksView.as_view(), name='my_feedbacks'),
    path('<int:feedback_id>/reply/', views.ReplyFeedbackView.as_view(), name='reply_feedback'),
    path('notifications/mark-read/', views.MarkNotificationsReadView.as_view(), name='mark_notifications_read'),
    path('notifications/unread-count/', views.UnreadNotificationCountView.as_view(), name='unread_count'),
]
