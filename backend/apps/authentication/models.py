from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginLog(models.Model):
    """Login log model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    ip_address = models.GenericIPAddressField(verbose_name='IP Address')
    user_agent = models.TextField(verbose_name='User Agent')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='Login Time')
    is_success = models.BooleanField(default=True, verbose_name='Is Success')
    failure_reason = models.CharField(max_length=200, blank=True, verbose_name='Failure Reason')

    class Meta:
        db_table = 'login_logs'
        verbose_name = 'Login Log'
        verbose_name_plural = 'Login Logs'
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


class VerificationCode(models.Model):
    """Verification code model"""
    CODE_TYPE_CHOICES = [
        ('register', 'Register'),
        ('login', 'Login'),
        ('reset_password', 'Reset Password'),
        ('change_phone', 'Change Phone'),
    ]

    phone = models.CharField(max_length=11, verbose_name='Phone')
    code = models.CharField(max_length=6, verbose_name='Code')
    code_type = models.CharField(max_length=20, choices=CODE_TYPE_CHOICES, verbose_name='Code Type')
    is_used = models.BooleanField(default=False, verbose_name='Is Used')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    expires_at = models.DateTimeField(verbose_name='Expires At')

    class Meta:
        db_table = 'verification_codes'
        verbose_name = 'Verification Code'
        verbose_name_plural = 'Verification Codes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.phone} - {self.code} ({self.get_code_type_display()})"

    def is_expired(self):
        """Check if verification code is expired"""
        from django.utils import timezone
        return timezone.now() > self.expires_at
