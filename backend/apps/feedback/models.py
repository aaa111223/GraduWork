from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FeedbackCategory(models.Model):
    """Feedback category model"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Category Name')
    description = models.TextField(blank=True, verbose_name='Description')
    sort_order = models.IntegerField(default=0, verbose_name='Sort Order')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        db_table = 'feedback_categories'
        verbose_name = 'Feedback Category'
        verbose_name_plural = 'Feedback Categories'
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name


class Feedback(models.Model):
    """Feedback model"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    # Basic info
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    category = models.ForeignKey(FeedbackCategory, on_delete=models.SET_NULL, null=True, verbose_name='Category')
    title = models.CharField(max_length=200, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    
    # Attachments
    attachments = models.JSONField(default=list, verbose_name='Attachments')
    
    # Contact info
    contact_phone = models.CharField(max_length=11, blank=True, verbose_name='Contact Phone')
    contact_email = models.EmailField(blank=True, verbose_name='Contact Email')
    
    # Processing info
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name='Priority')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='assigned_feedbacks', verbose_name='Assigned To')
    
    # Results
    admin_reply = models.TextField(blank=True, verbose_name='Admin Reply')
    resolution = models.TextField(blank=True, verbose_name='Resolution')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    resolved_at = models.DateTimeField(blank=True, null=True, verbose_name='Resolved At')
    
    class Meta:
        db_table = 'feedbacks'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.phone} - {self.title}"


class FeedbackReply(models.Model):
    """Feedback reply model"""
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='replies', verbose_name='Feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    content = models.TextField(verbose_name='Content')
    attachments = models.JSONField(default=list, verbose_name='Attachments')
    is_admin_reply = models.BooleanField(default=False, verbose_name='Is Admin Reply')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        db_table = 'feedback_replies'
        verbose_name = 'Feedback Reply'
        verbose_name_plural = 'Feedback Replies'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.phone} replies to {self.feedback.title}"


class SystemNotification(models.Model):
    """System notification model"""
    NOTIFICATION_TYPE_CHOICES = [
        ('system', 'System'),
        ('job', 'Job Related'),
        ('application', 'Application Related'),
        ('interview', 'Interview Related'),
        ('feedback', 'Feedback Related'),
    ]
    
    # Basic info
    title = models.CharField(max_length=200, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, verbose_name='Type')
    
    # Recipient
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Recipient')
    
    # Status
    is_read = models.BooleanField(default=False, verbose_name='Is Read')
    read_at = models.DateTimeField(blank=True, null=True, verbose_name='Read At')
    
    # Related object
    related_object_id = models.IntegerField(blank=True, null=True, verbose_name='Related Object ID')
    related_object_type = models.CharField(max_length=50, blank=True, verbose_name='Related Object Type')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        db_table = 'system_notifications'
        verbose_name = 'System Notification'
        verbose_name_plural = 'System Notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient.phone} - {self.title}"
    
    def mark_as_read(self):
        """Mark as read"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
