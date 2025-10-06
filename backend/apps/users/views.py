from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from django.http import HttpResponse, Http404
import os
from .models import User, Role, StudentProfile, EnterpriseProfile, JobIntention, Resume
from .serializers import (
    UserSerializer, RoleSerializer, StudentProfileSerializer,
    EnterpriseProfileSerializer, UserLoginSerializer, UserRegistrationSerializer,
    JobIntentionSerializer, ResumeSerializer, UserProfileSerializer, UserUpdateSerializer
)


class UserRegistrationView(APIView):
    """User registration view"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user_id': user.id,
                'phone': user.phone
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login view"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """User logout view"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    """User ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'profile':
            return UserProfileSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile with related data"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # 返回完整的用户信息
            profile_serializer = UserProfileSerializer(request.user)
            return Response(profile_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_avatar(self, request):
        """Upload user avatar"""
        if 'avatar' not in request.FILES:
            return Response({'error': 'No avatar file provided'}, status=status.HTTP_400_BAD_REQUEST)

        avatar_file = request.FILES['avatar']

        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if avatar_file.content_type not in allowed_types:
            return Response({'error': 'Invalid file type. Only JPEG, PNG, and GIF are allowed.'},
                          status=status.HTTP_400_BAD_REQUEST)

        # 验证文件大小 (最大5MB)
        if avatar_file.size > 5 * 1024 * 1024:
            return Response({'error': 'File size too large. Maximum 5MB allowed.'},
                          status=status.HTTP_400_BAD_REQUEST)

        # 保存头像
        request.user.avatar = avatar_file
        request.user.save()

        # 返回完整的用户信息
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get', 'post', 'put', 'patch'])
    def job_intention(self, request):
        """Manage user job intention"""
        if request.method == 'GET':
            try:
                intention = JobIntention.objects.get(user=request.user)
                serializer = JobIntentionSerializer(intention)
                return Response(serializer.data)
            except JobIntention.DoesNotExist:
                return Response({'message': 'No job intention found'}, status=status.HTTP_404_NOT_FOUND)

        elif request.method in ['POST', 'PUT', 'PATCH']:
            try:
                intention = JobIntention.objects.get(user=request.user)
                serializer = JobIntentionSerializer(intention, data=request.data, partial=request.method == 'PATCH')
            except JobIntention.DoesNotExist:
                serializer = JobIntentionSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'post'], parser_classes=[MultiPartParser, FormParser])
    def resumes(self, request):
        """Manage user resumes"""
        if request.method == 'GET':
            resumes = Resume.objects.filter(user=request.user)
            serializer = ResumeSerializer(resumes, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            file = request.FILES.get('file')
            name = request.data.get('name', file.name if file else 'Untitled Resume')

            if not file:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate file type
            allowed_types = ['pdf', 'doc', 'docx']
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in allowed_types:
                return Response({'error': 'Invalid file type. Only PDF, DOC, DOCX are allowed.'},
                              status=status.HTTP_400_BAD_REQUEST)

            # Validate file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                return Response({'error': 'File size too large. Maximum 10MB allowed.'},
                              status=status.HTTP_400_BAD_REQUEST)

            resume = Resume.objects.create(
                user=request.user,
                name=name,
                file=file,
                file_size=file.size,
                file_type=file_extension,
                is_default=request.data.get('is_default', False)
            )

            serializer = ResumeSerializer(resume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get', 'delete'], url_path='resumes/(?P<resume_id>[^/.]+)')
    def resume_detail(self, request, resume_id=None):
        """Get or delete specific resume"""
        try:
            resume = Resume.objects.get(id=resume_id, user=request.user)
        except Resume.DoesNotExist:
            return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            # Return file for download
            if resume.file and default_storage.exists(resume.file.name):
                response = HttpResponse(resume.file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{resume.name}"'
                return response
            else:
                return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        elif request.method == 'DELETE':
            # Delete file from storage
            if resume.file and default_storage.exists(resume.file.name):
                default_storage.delete(resume.file.name)
            resume.delete()
            return Response({'message': 'Resume deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class RoleViewSet(ModelViewSet):
    """Role ViewSet"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class StudentProfileViewSet(ModelViewSet):
    """Student Profile ViewSet"""
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['put', 'patch'])
    def update_current(self, request):
        """Update current user's student profile"""
        try:
            # 获取或创建当前用户的学生档案
            student_profile, created = StudentProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'student_id': '',
                    'school': '',
                    'major': '',
                    'grade': '',
                    'gpa': None
                }
            )

            serializer = StudentProfileSerializer(student_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        """Filter by current user if not admin"""
        if self.request.user.has_role('admin') or self.request.user.has_role('super_admin'):
            return StudentProfile.objects.all()
        return StudentProfile.objects.filter(user=self.request.user)


class EnterpriseProfileViewSet(ModelViewSet):
    """Enterprise Profile ViewSet"""
    queryset = EnterpriseProfile.objects.all()
    serializer_class = EnterpriseProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter by current user if not admin"""
        if self.request.user.has_role('admin') or self.request.user.has_role('super_admin'):
            return EnterpriseProfile.objects.all()
        return EnterpriseProfile.objects.filter(user=self.request.user)
