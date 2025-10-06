from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class JobApplication(models.Model):
    """Job application model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Reviewing'),
        ('interview', 'Interview'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    # Basic info
    applicant = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE, verbose_name='Applicant')
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, verbose_name='Job')
    
    # Application info
    cover_letter = models.TextField(blank=True, verbose_name='Cover Letter')
    resume = models.FileField(upload_to='applications/resumes/', blank=True, null=True, verbose_name='Resume')
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Expected Salary')
    
    # Status info
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    hr_notes = models.TextField(blank=True, verbose_name='HR Notes')
    rejection_reason = models.TextField(blank=True, verbose_name='Rejection Reason')
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name='Applied At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    reviewed_at = models.DateTimeField(blank=True, null=True, verbose_name='Reviewed At')
    
    class Meta:
        db_table = 'job_applications'
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        unique_together = ['applicant', 'job']
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.applicant.user.real_name} applies for {self.job.title}"


class Interview(models.Model):
    """Interview model"""
    INTERVIEW_TYPE_CHOICES = [
        ('phone', 'Phone Interview'),
        ('video', 'Video Interview'),
        ('onsite', 'Onsite Interview'),
        ('group', 'Group Interview'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    # Basic info
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, verbose_name='Application')
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Interviewer')
    
    # Interview info
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES, verbose_name='Interview Type')
    scheduled_time = models.DateTimeField(verbose_name='Scheduled Time')
    duration = models.IntegerField(default=60, verbose_name='Duration (minutes)')
    location = models.TextField(blank=True, verbose_name='Location/Link')
    
    # Results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name='Status')
    score = models.IntegerField(blank=True, null=True, verbose_name='Score')
    feedback = models.TextField(blank=True, verbose_name='Feedback')
    notes = models.TextField(blank=True, verbose_name='Notes')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        db_table = 'interviews'
        verbose_name = 'Interview'
        verbose_name_plural = 'Interviews'
        ordering = ['-scheduled_time']
    
    def __str__(self):
        return f"{self.application.applicant.user.real_name} - {self.application.job.title} Interview"


class ApplicationStatusLog(models.Model):
    """Application status log model"""
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, verbose_name='Application')
    old_status = models.CharField(max_length=20, verbose_name='Old Status')
    new_status = models.CharField(max_length=20, verbose_name='New Status')
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Changed By')
    reason = models.TextField(blank=True, verbose_name='Reason')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        db_table = 'application_status_logs'
        verbose_name = 'Application Status Log'
        verbose_name_plural = 'Application Status Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.application} status changed: {self.old_status} -> {self.new_status}"
