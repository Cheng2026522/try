from django.db import models
from django.conf import settings

class FileCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '文件分类'
        verbose_name_plural = '文件分类'

class UploadedFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('document', '文档'),
        ('image', '图片'),
        ('spreadsheet', '表格'),
        ('other', '其他'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='上传用户')
    category = models.ForeignKey(FileCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='分类')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name='文件')
    filename = models.CharField(max_length=255, verbose_name='文件名')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='document', verbose_name='文件类型')
    size = models.BigIntegerField(verbose_name='文件大小')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    is_analyzed = models.BooleanField(default=False, verbose_name='是否已分析')
    
    def __str__(self):
        return self.filename
    
    class Meta:
        verbose_name = '上传文件'
        verbose_name_plural = '上传文件'
