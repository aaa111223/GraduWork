from rest_framework import serializers
from .models import Feedback, FeedbackCategory, FeedbackReply, SystemNotification
from apps.users.serializers import UserBasicSerializer


class FeedbackCategorySerializer(serializers.ModelSerializer):
    """Feedback category serializer"""
    class Meta:
        model = FeedbackCategory
        fields = ['id', 'name', 'description', 'sort_order', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class FeedbackReplySerializer(serializers.ModelSerializer):
    """Feedback reply serializer"""
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = FeedbackReply
        fields = ['id', 'user', 'content', 'attachments', 'is_admin_reply', 'created_at']
        read_only_fields = ['id', 'user', 'is_admin_reply', 'created_at']


class FeedbackListSerializer(serializers.ModelSerializer):
    """Feedback list serializer"""
    user = UserBasicSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    status_display = serializers.SerializerMethodField()
    priority_display = serializers.SerializerMethodField()
    has_reply = serializers.SerializerMethodField()
    
    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'category', 'category_name', 'title', 'content',
            'status', 'status_display', 'priority', 'priority_display',
            'has_reply', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_status_display(self, obj):
        status_map = {
            'pending': '待处理',
            'processing': '处理中',
            'resolved': '已解决',
            'closed': '已关闭'
        }
        return status_map.get(obj.status, obj.status)
    
    def get_priority_display(self, obj):
        priority_map = {
            'low': '低',
            'medium': '中',
            'high': '高',
            'urgent': '紧急'
        }
        return priority_map.get(obj.priority, obj.priority)
    
    def get_has_reply(self, obj):
        return bool(obj.admin_reply) or obj.replies.filter(is_admin_reply=True).exists()


class FeedbackDetailSerializer(serializers.ModelSerializer):
    """Feedback detail serializer"""
    user = UserBasicSerializer(read_only=True)
    category = FeedbackCategorySerializer(read_only=True)
    replies = FeedbackReplySerializer(many=True, read_only=True)
    status_display = serializers.SerializerMethodField()
    priority_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'category', 'title', 'content', 'attachments',
            'contact_phone', 'contact_email', 'priority', 'priority_display',
            'status', 'status_display', 'admin_reply', 'resolution',
            'replies', 'created_at', 'updated_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'resolved_at']
    
    def get_status_display(self, obj):
        status_map = {
            'pending': '待处理',
            'processing': '处理中',
            'resolved': '已解决',
            'closed': '已关闭'
        }
        return status_map.get(obj.status, obj.status)
    
    def get_priority_display(self, obj):
        priority_map = {
            'low': '低',
            'medium': '中',
            'high': '高',
            'urgent': '紧急'
        }
        return priority_map.get(obj.priority, obj.priority)


class FeedbackCreateSerializer(serializers.ModelSerializer):
    """Feedback create serializer"""
    category_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Feedback
        fields = [
            'category_id', 'title', 'content', 'attachments',
            'contact_phone', 'contact_email', 'priority'
        ]
    
    def validate_category_id(self, value):
        if value and not FeedbackCategory.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("无效的反馈分类")
        return value
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        feedback = Feedback.objects.create(
            user=self.context['request'].user,
            category_id=category_id,
            **validated_data
        )
        return feedback


class SystemNotificationSerializer(serializers.ModelSerializer):
    """System notification serializer"""
    recipient = UserBasicSerializer(read_only=True)
    type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = SystemNotification
        fields = [
            'id', 'title', 'content', 'notification_type', 'type_display',
            'recipient', 'is_read', 'read_at', 'related_object_id',
            'related_object_type', 'created_at'
        ]
        read_only_fields = ['id', 'recipient', 'created_at']
    
    def get_type_display(self, obj):
        type_map = {
            'system': '系统通知',
            'job': '职位相关',
            'application': '申请相关',
            'interview': '面试相关',
            'feedback': '反馈相关'
        }
        return type_map.get(obj.notification_type, obj.notification_type)
