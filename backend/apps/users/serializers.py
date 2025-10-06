from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Role, StudentProfile, EnterpriseProfile, JobIntention, Resume


class RoleSerializer(serializers.ModelSerializer):
    """Role serializer"""
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for references"""
    class Meta:
        model = User
        fields = ['id', 'phone', 'real_name', 'user_type']
        read_only_fields = ['id', 'phone', 'real_name', 'user_type']


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    roles = RoleSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'phone', 'email', 'user_type', 'avatar', 'real_name', 
            'gender', 'birth_date', 'address', 'roles', 'is_verified',
            'is_active', 'is_staff', 'created_at', 'updated_at',
            'password', 'password_confirm'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
        }
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if 'password' in attrs and 'password_confirm' in attrs:
            if attrs['password'] != attrs['password_confirm']:
                raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        """Create user with encrypted password"""
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer"""
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Validate user credentials"""
        phone = attrs.get('phone')
        password = attrs.get('password')
        
        if phone and password:
            user = authenticate(username=phone, password=password)
            if not user:
                raise serializers.ValidationError('Invalid phone or password')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include phone and password')
        
        return attrs


class StudentProfileSerializer(serializers.ModelSerializer):
    """Student profile serializer"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'student_id', 'school', 'major', 'grade',
            'graduation_date', 'gpa', 'resume', 'skills', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_gpa(self, value):
        """Validate GPA range"""
        if value is not None:
            if value < 0 or value > 4:
                raise serializers.ValidationError("GPA must be between 0.0 and 4.0")
        return value


class EnterpriseProfileSerializer(serializers.ModelSerializer):
    """Enterprise profile serializer"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = EnterpriseProfile
        fields = [
            'id', 'user', 'company_name', 'company_code', 'industry',
            'company_size', 'company_address', 'company_website',
            'company_description', 'business_license', 'is_verified',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'phone', 'email', 'user_type', 'real_name', 'gender',
            'password', 'password_confirm'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
        }

    def validate(self, attrs):
        """Validate registration data"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        """Create new user account"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class JobIntentionSerializer(serializers.ModelSerializer):
    """Job intention serializer"""

    class Meta:
        model = JobIntention
        fields = [
            'id', 'position', 'salary_range', 'work_cities', 'job_type',
            'industry', 'company_size', 'other_requirements', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ResumeSerializer(serializers.ModelSerializer):
    """Resume serializer"""
    file_size_display = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = [
            'id', 'name', 'file', 'file_size', 'file_size_display', 'file_type',
            'is_default', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'file_size', 'file_type', 'created_at', 'updated_at']

    def get_file_size_display(self, obj):
        """Convert file size to human readable format"""
        size = obj.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"


class UserUpdateSerializer(serializers.ModelSerializer):
    """User update serializer for profile updates"""

    class Meta:
        model = User
        fields = [
            'email', 'real_name', 'gender', 'birth_date', 'address'
        ]

    def validate_email(self, value):
        """Validate email uniqueness"""
        if value and User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer with related data"""
    student_profile = StudentProfileSerializer(source='studentprofile', read_only=True)
    enterprise_profile = EnterpriseProfileSerializer(source='enterpriseprofile', read_only=True)
    job_intention = JobIntentionSerializer(source='jobintention', read_only=True)
    resumes = ResumeSerializer(source='resume_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'phone', 'email', 'user_type', 'avatar', 'real_name',
            'gender', 'birth_date', 'address', 'is_verified', 'is_active',
            'created_at', 'updated_at', 'student_profile', 'enterprise_profile',
            'job_intention', 'resumes'
        ]
        read_only_fields = ['id', 'phone', 'user_type', 'is_verified', 'created_at', 'updated_at']
