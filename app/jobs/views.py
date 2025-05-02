from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import JobPost
from .serializers import JobPostSerializer
from .filters import JobPostFilter
from django.db.models import Q  # Required import

from rest_framework import filters


class TestView(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response({"detail": "Success"})


class JobPostViewSet(viewsets.ViewSet):
    """
    Custom ViewSet for job postings.
    """

    queryset = JobPost.objects.all().order_by("-created_at")

    # permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = JobPostFilter
    ordering_fields = ["created_at", "salary_amount"]
    ordering = ["-created_at"]
    search_fields = [
        "title",
    ]

    def list(self, request):
        queryset = JobPost.objects.all().order_by("-created_at")

        # Only show approved for non-admin users
        if not request.user.is_admin:
            queryset = queryset.filter(status="approved")

        # Apply your filters first
        filtered = JobPostFilter(request.GET, queryset=queryset).qs

        # Handle search
        search_query = request.GET.get("search")
        if search_query:
            filtered = filtered.filter(
                Q(title__icontains=search_query)
                | Q(company_name__icontains=search_query)
                | Q(location__icontains=search_query)
                | Q(category__icontains=search_query)
                | Q(tags__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        serializer = JobPostSerializer(filtered, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        job = get_object_or_404(JobPost, pk=pk)
        if job.status != "approved" and not request.user.is_staff:
            return Response({"detail": "Not authorized to view this job."}, status=403)

        serializer = JobPostSerializer(job)
        return Response(serializer.data)

    def create(self, request):
        serializer = JobPostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        job = get_object_or_404(JobPost, pk=pk)
        if request.user != job.creator and not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=403)

        serializer = JobPostSerializer(
            job, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        job = get_object_or_404(JobPost, pk=pk)
        if request.user != job.creator and not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=403)
        job.delete()
        return Response(status=204)

    @action(detail=True, methods=["post"])
    def mark_unavailable(self, request, pk=None):
        job = get_object_or_404(JobPost, pk=pk)
        if request.user in job.marked_unavailable_by.all():
            return Response({"detail": "Already marked unavailable."}, status=400)

        job.mark_unavailable(request.user)
        return Response({"detail": "Marked as unavailable."})

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        job = get_object_or_404(JobPost, pk=pk)
        job.status = "approved"
        job.save()
        return Response({"detail": "Job approved."})

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        job = get_object_or_404(JobPost, pk=pk)
        job.status = "rejected"
        job.save()
        return Response({"detail": "Job rejected."})
