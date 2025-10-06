# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import JobCategory, Job, JobFavorite


class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.all()
    permission_classes = [AllowAny]  # ùùùù?ùùºù˚ùùùùù

    def list(self, request):
        return Response({'message': 'Job category list endpoint'}, status=status.HTTP_200_OK)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = [AllowAny]  # ùùùù?ùùºù˚ùùùùù

    def list(self, request):
        # ????????
        mock_jobs = [
            {
                'id': 1,
                'title': 'Python???????',
                'company_name': '??????',
                'location': '???',
                'salary_range': '15K-25K',
                'experience_required': '3-5?',
                'education_required': '??',
                'job_type': 'full_time',
                'description': '???????????',
                'requirements': 'Python, Django, MySQL',
                'created_at': '2025-09-20T10:00:00Z',
                'updated_at': '2025-09-20T10:00:00Z'
            },
            {
                'id': 2,
                'title': 'Vue.js???????',
                'company_name': '???????',
                'location': '???',
                'salary_range': '12K-20K',
                'experience_required': '2-4?',
                'education_required': '??',
                'job_type': 'full_time',
                'description': '???????????????',
                'requirements': 'Vue.js, JavaScript, CSS',
                'created_at': '2025-09-19T14:30:00Z',
                'updated_at': '2025-09-19T14:30:00Z'
            },
            {
                'id': 3,
                'title': '????',
                'company_name': '??????',
                'location': '???',
                'salary_range': '18K-30K',
                'experience_required': '3-6?',
                'education_required': '??',
                'job_type': 'full_time',
                'description': '???????????',
                'requirements': '????, ????, ????',
                'created_at': '2025-09-18T09:15:00Z',
                'updated_at': '2025-09-18T09:15:00Z'
            }
        ]
        return Response({
            'count': len(mock_jobs),
            'results': mock_jobs
        }, status=status.HTTP_200_OK)

    def create(self, request):
        return Response({'message': 'Create job endpoint'}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        return Response({'message': 'Job detail endpoint'}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        return Response({'message': 'Update job endpoint'}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        return Response({'message': 'Delete job endpoint'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        return Response({'message': 'Favorite job endpoint'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def unfavorite(self, request, pk=None):
        return Response({'message': 'Unfavorite job endpoint'}, status=status.HTTP_200_OK)


class JobFavoriteViewSet(viewsets.ModelViewSet):
    queryset = JobFavorite.objects.all()

    def list(self, request):
        return Response({'message': 'Job favorite list endpoint'}, status=status.HTTP_200_OK)


class JobSearchView(APIView):
    def get(self, request):
        return Response({'message': 'Job search endpoint'}, status=status.HTTP_200_OK)


class JobRecommendationView(APIView):
    def get(self, request):
        return Response({'message': 'Job recommendation endpoint'}, status=status.HTTP_200_OK)


class ToggleFavoriteView(APIView):
    def post(self, request, job_id):
        return Response({'message': 'Toggle favorite endpoint'}, status=status.HTTP_200_OK)
