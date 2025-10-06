from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for phone-based authentication"""

    def create_user(self, phone, email=None, password=None, **extra_fields):
        """Create and save a regular user with the given phone and password"""
        if not phone:
            raise ValueError('The Phone field must be set')

        email = self.normalize_email(email) if email else None
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        """Create and save a superuser with the given phone and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, email, password, **extra_fields)


class Role(models.Model):
    """Role model"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('enterprise', 'Enterprise HR'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True, verbose_name='Role Name')
    description = models.TextField(blank=True, verbose_name='Description')
    permissions = models.JSONField(default=list, verbose_name='Permissions')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    """Custom user model"""
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('enterprise', 'Enterprise HR'),
        ('admin', 'Admin'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    # Remove the default username field
    username = None

    # Override email field to make it optional
    email = models.EmailField(blank=True, null=True, verbose_name='Email')

    # Basic info
    phone = models.CharField(max_length=11, unique=True, verbose_name='Phone')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, verbose_name='User Type')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')

    # Personal info
    real_name = models.CharField(max_length=50, blank=True, verbose_name='Real Name')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='Gender')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Birth Date')

    # Contact info
    address = models.TextField(blank=True, verbose_name='Address')

    # Roles and permissions
    roles = models.ManyToManyField(Role, blank=True, verbose_name='Roles')

    # Status info
    is_verified = models.BooleanField(default=False, verbose_name='Is Verified')
    last_login_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='Last Login IP')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    # Use phone as username
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'user_type']

    # Use custom user manager
    objects = UserManager()
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.phone} ({self.get_user_type_display()})"
    
    def has_role(self, role_name):
        """Check if user has specific role"""
        return self.roles.filter(name=role_name).exists()
    
    def get_permissions(self):
        """Get all user permissions"""
        permissions = set()
        for role in self.roles.all():
            permissions.update(role.permissions)
        return list(permissions)


class StudentProfile(models.Model):
    """Student profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='Student ID')
    school = models.CharField(max_length=100, verbose_name='School')
    major = models.CharField(max_length=100, verbose_name='Major')
    grade = models.CharField(max_length=10, verbose_name='Grade')
    graduation_date = models.DateField(blank=True, null=True, verbose_name='Graduation Date')
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, verbose_name='GPA')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, verbose_name='Resume')
    skills = models.JSONField(default=list, verbose_name='Skills')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        db_table = 'student_profiles'
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return f"{self.user.real_name} - {self.student_id}"


class JobIntention(models.Model):
    """Job intention model for students"""
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]

    SALARY_RANGE_CHOICES = [
        ('3K-5K', '3K-5K'),
        ('5K-10K', '5K-10K'),
        ('10K-15K', '10K-15K'),
        ('15K-25K', '15K-25K'),
        ('25K-35K', '25K-35K'),
        ('35K+', '35K以上'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    position = models.CharField(max_length=100, verbose_name='Expected Position')
    salary_range = models.CharField(max_length=20, choices=SALARY_RANGE_CHOICES, verbose_name='Expected Salary')
    work_cities = models.JSONField(default=list, verbose_name='Preferred Cities')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time', verbose_name='Job Type')
    industry = models.CharField(max_length=100, blank=True, verbose_name='Preferred Industry')
    company_size = models.CharField(max_length=50, blank=True, verbose_name='Preferred Company Size')
    other_requirements = models.TextField(blank=True, verbose_name='Other Requirements')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        db_table = 'job_intentions'
        verbose_name = 'Job Intention'
        verbose_name_plural = 'Job Intentions'

    def __str__(self):
        return f"{self.user.real_name} - {self.position}"


class Resume(models.Model):
    """Resume model for file management"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    name = models.CharField(max_length=200, verbose_name='Resume Name')
    file = models.FileField(upload_to='resumes/', verbose_name='Resume File')
    file_size = models.IntegerField(verbose_name='File Size (bytes)')
    file_type = models.CharField(max_length=10, verbose_name='File Type')
    is_default = models.BooleanField(default=False, verbose_name='Is Default Resume')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        db_table = 'resumes'
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.real_name} - {self.name}"

    def save(self, *args, **kwargs):
        # 如果设置为默认简历，取消其他简历的默认状态
        if self.is_default:
            Resume.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class EnterpriseProfile(models.Model):
    """Enterprise profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    company_name = models.CharField(max_length=200, verbose_name='Company Name')
    company_code = models.CharField(max_length=50, unique=True, verbose_name='Company Code')
    industry = models.CharField(max_length=100, verbose_name='Industry')
    company_size = models.CharField(max_length=50, verbose_name='Company Size')
    company_address = models.TextField(verbose_name='Company Address')
    company_website = models.URLField(blank=True, verbose_name='Company Website')
    company_description = models.TextField(blank=True, verbose_name='Company Description')
    business_license = models.FileField(upload_to='licenses/', verbose_name='Business License')
    is_verified = models.BooleanField(default=False, verbose_name='Is Verified')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        db_table = 'enterprise_profiles'
        verbose_name = 'Enterprise Profile'
        verbose_name_plural = 'Enterprise Profiles'
    
    def __str__(self):
        return f"{self.company_name} - {self.user.real_name}"
