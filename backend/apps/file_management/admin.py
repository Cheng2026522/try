from django.contrib import admin
from .models import FileCategory, UploadedFile

@admin.register(FileCategory)
class FileCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'user', 'category', 'file_type', 'size', 'is_analyzed', 'uploaded_at']
    list_filter = ['file_type', 'is_analyzed', 'category', 'uploaded_at']
    search_fields = ['filename', 'description']
    raw_id_fields = ['user', 'category']
    readonly_fields = ['uploaded_at']
