from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class JobCategory(models.Model):
    """Job category model"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Category Name')
    description = models.TextField(blank=True, verbose_name='Description')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Parent Category')
    sort_order = models.IntegerField(default=0, verbose_name='Sort Order')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        db_table = 'job_categories'
        verbose_name = 'Job Category'
        verbose_name_plural = 'Job Categories'
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name


class Job(models.Model):
    """Job model"""
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]
    
    SALARY_TYPE_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('hourly', 'Hourly'),
        ('negotiable', 'Negotiable'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('paused', 'Paused'),
        ('closed', 'Closed'),
    ]
    
    # Basic info
    title = models.CharField(max_length=200, verbose_name='Job Title')
    company = models.ForeignKey('users.EnterpriseProfile', on_delete=models.CASCADE, verbose_name='Company')
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, verbose_name='Category')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, verbose_name='Job Type')
    
    # Salary info
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Min Salary')
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Max Salary')
    salary_type = models.CharField(max_length=20, choices=SALARY_TYPE_CHOICES, default='monthly', verbose_name='Salary Type')
    
    # Location
    work_city = models.CharField(max_length=100, verbose_name='Work City')
    work_address = models.TextField(verbose_name='Work Address')
    
    # Requirements
    experience_required = models.CharField(max_length=100, blank=True, verbose_name='Experience Required')
    education_required = models.CharField(max_length=100, blank=True, verbose_name='Education Required')
    skills_required = models.JSONField(default=list, verbose_name='Skills Required')
    
    # Description
    description = models.TextField(verbose_name='Job Description')
    responsibilities = models.TextField(verbose_name='Responsibilities')
    benefits = models.TextField(blank=True, verbose_name='Benefits')
    
    # Recruitment info
    recruitment_count = models.IntegerField(default=1, verbose_name='Recruitment Count')
    application_deadline = models.DateTimeField(blank=True, null=True, verbose_name='Application Deadline')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Status')
    view_count = models.IntegerField(default=0, verbose_name='View Count')
    application_count = models.IntegerField(default=0, verbose_name='Application Count')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='Published At')
    
    class Meta:
        db_table = 'jobs'
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.company.company_name}"
    
    def is_active(self):
        """Check if job is active"""
        from django.utils import timezone
        if self.status != 'published':
            return False
        if self.application_deadline and timezone.now() > self.application_deadline:
            return False
        return True


class JobFavorite(models.Model):
    """Job favorite model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='Job')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        db_table = 'job_favorites'
        verbose_name = 'Job Favorite'
        verbose_name_plural = 'Job Favorites'
        unique_together = ['user', 'job']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.phone} favorites {self.job.title}"
