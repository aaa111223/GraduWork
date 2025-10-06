from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
from .models import Feedback, FeedbackCategory, FeedbackReply, SystemNotification
from .serializers import (
    FeedbackCategorySerializer, FeedbackListSerializer, FeedbackDetailSerializer,
    FeedbackCreateSerializer, FeedbackReplySerializer, SystemNotificationSerializer
)


class FeedbackCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Feedback category viewset"""
    queryset = FeedbackCategory.objects.filter(is_active=True).order_by('sort_order', 'name')
    serializer_class = FeedbackCategorySerializer
    permission_classes = [IsAuthenticated]


class FeedbackViewSet(viewsets.ModelViewSet):
    """Feedback viewset"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get user's feedbacks"""
        return Feedback.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        """Get appropriate serializer class"""
        if self.action == 'create':
            return FeedbackCreateSerializer
        elif self.action == 'retrieve':
            return FeedbackDetailSerializer
        return FeedbackListSerializer

    def create(self, request):
        """Create new feedback"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()
            return Response(
                FeedbackDetailSerializer(feedback).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """Reply to feedback (for admin use)"""
        feedback = self.get_object()
        content = request.data.get('content')

        if not content:
            return Response(
                {'error': '回复内容不能为空'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create reply
        reply = FeedbackReply.objects.create(
            feedback=feedback,
            user=request.user,
            content=content,
            is_admin_reply=request.user.is_staff
        )

        # Update feedback status
        if request.user.is_staff:
            feedback.status = 'resolved'
            feedback.resolved_at = timezone.now()
            feedback.save()

        return Response(
            FeedbackReplySerializer(reply).data,
            status=status.HTTP_201_CREATED
        )


class FeedbackReplyViewSet(viewsets.ReadOnlyModelViewSet):
    """Feedback reply viewset"""
    serializer_class = FeedbackReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get replies for user's feedbacks"""
        user_feedback_ids = Feedback.objects.filter(user=self.request.user).values_list('id', flat=True)
        return FeedbackReply.objects.filter(feedback_id__in=user_feedback_ids).order_by('created_at')


class SystemNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """System notification viewset"""
    serializer_class = SystemNotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get user's notifications"""
        return SystemNotification.objects.filter(recipient=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'message': '通知已标记为已读'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        notifications = self.get_queryset().filter(is_read=False)
        for notification in notifications:
            notification.mark_as_read()
        return Response({'message': '所有通知已标记为已读'}, status=status.HTTP_200_OK)


class MyFeedbacksView(APIView):
    """Get user's feedbacks"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
        serializer = FeedbackListSerializer(feedbacks, many=True)
        return Response({
            'results': serializer.data,
            'count': feedbacks.count()
        }, status=status.HTTP_200_OK)


class ReplyFeedbackView(APIView):
    """Reply to feedback"""
    permission_classes = [IsAuthenticated]

    def post(self, request, feedback_id):
        try:
            feedback = Feedback.objects.get(id=feedback_id, user=request.user)
        except Feedback.DoesNotExist:
            return Response({'error': '反馈不存在'}, status=status.HTTP_404_NOT_FOUND)

        content = request.data.get('content')
        if not content:
            return Response({'error': '回复内容不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        reply = FeedbackReply.objects.create(
            feedback=feedback,
            user=request.user,
            content=content,
            is_admin_reply=False
        )

        return Response(
            FeedbackReplySerializer(reply).data,
            status=status.HTTP_201_CREATED
        )


class MarkNotificationsReadView(APIView):
    """Mark notifications as read"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        notification_ids = request.data.get('notification_ids', [])
        if notification_ids:
            notifications = SystemNotification.objects.filter(
                id__in=notification_ids,
                recipient=request.user,
                is_read=False
            )
        else:
            notifications = SystemNotification.objects.filter(
                recipient=request.user,
                is_read=False
            )

        for notification in notifications:
            notification.mark_as_read()

        return Response({
            'message': f'已标记 {notifications.count()} 条通知为已读'
        }, status=status.HTTP_200_OK)


class UnreadNotificationCountView(APIView):
    """Get unread notification count"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = SystemNotification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        return Response({'count': count}, status=status.HTTP_200_OK)
