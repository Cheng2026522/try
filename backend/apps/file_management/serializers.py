from rest_framework import serializers
from .models import FileCategory, UploadedFile

class FileCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FileCategory
        fields = ['id', 'name', 'description', 'created_at']

class UploadedFileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UploadedFile
        fields = ['id', 'user', 'category', 'category_name', 'file', 'file_url', 'filename', 'file_type', 'size', 'description', 'uploaded_at', 'is_analyzed']
        read_only_fields = ['user', 'uploaded_at', 'is_analyzed', 'size']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
