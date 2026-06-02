from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import FileCategory, UploadedFile
from .serializers import FileCategorySerializer, UploadedFileSerializer
from django.http import FileResponse
import os

class FileCategoryViewSet(viewsets.ModelViewSet):
    queryset = FileCategory.objects.all()
    serializer_class = FileCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = UploadedFile.objects.all()
        user = self.request.user
        if not user.is_superuser and user.role != 'admin':
            queryset = queryset.filter(user=user)
        return queryset
    
    def perform_create(self, serializer):
        file = self.request.data.get('file')
        serializer.save(
            user=self.request.user,
            size=file.size,
            filename=file.name
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = instance.file.path
        self.perform_destroy(instance)
        if os.path.exists(file_path):
            os.remove(file_path)
        return Response(status=status.HTTP_204_NO_CONTENT)

class FileDownloadView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def retrieve(self, request, pk=None):
        try:
            uploaded_file = UploadedFile.objects.get(pk=pk)
            if not request.user.is_superuser and uploaded_file.user != request.user:
                return Response({'detail': '无权访问'}, status=status.HTTP_403_FORBIDDEN)
            return FileResponse(uploaded_file.file.open(), as_attachment=True, filename=uploaded_file.filename)
        except UploadedFile.DoesNotExist:
            return Response({'detail': '文件不存在'}, status=status.HTTP_404_NOT_FOUND)
