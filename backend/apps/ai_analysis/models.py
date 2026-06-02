from django.db import models
from django.conf import settings
from apps.file_management.models import UploadedFile

class AIAnalysisResult(models.Model):
    ANALYSIS_STATUS_CHOICES = [
        ('pending', '待分析'),
        ('processing', '分析中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]
    
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, verbose_name='关联文件')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='操作用户')
    summary = models.TextField(blank=True, null=True, verbose_name='文档摘要')
    extracted_info = models.JSONField(blank=True, null=True, verbose_name='提取的关键信息')
    status = models.CharField(max_length=20, choices=ANALYSIS_STATUS_CHOICES, default='pending', verbose_name='分析状态')
    version = models.IntegerField(default=1, verbose_name='版本号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_selected = models.BooleanField(default=False, verbose_name='是否为选中版本')
    
    def __str__(self):
        return f'{self.file.filename} - 版本{self.version}'
    
    class Meta:
        verbose_name = 'AI分析结果'
        verbose_name_plural = 'AI分析结果'
        unique_together = ('file', 'version')

class AnalysisHistory(models.Model):
    analysis = models.ForeignKey(AIAnalysisResult, on_delete=models.CASCADE, verbose_name='关联分析')
    action = models.CharField(max_length=100, verbose_name='操作类型')
    action_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='操作者')
    details = models.JSONField(blank=True, null=True, verbose_name='操作详情')
    
    def __str__(self):
        return f'{self.analysis.file.filename} - {self.action}'
    
    class Meta:
        verbose_name = '分析历史'
        verbose_name_plural = '分析历史'
