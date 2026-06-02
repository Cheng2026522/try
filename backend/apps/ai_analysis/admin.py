from django.contrib import admin
from .models import AIAnalysisResult, AnalysisHistory

@admin.register(AIAnalysisResult)
class AIAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'user', 'status', 'version', 'is_selected', 'created_at']
    list_filter = ['status', 'is_selected', 'created_at']
    search_fields = ['file__filename', 'summary']
    raw_id_fields = ['file', 'user']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(AnalysisHistory)
class AnalysisHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'analysis', 'action', 'operator', 'action_time']
    list_filter = ['action', 'action_time']
    search_fields = ['action', 'details']
    raw_id_fields = ['analysis', 'operator']
    readonly_fields = ['action_time']
