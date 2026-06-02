from rest_framework import serializers
from .models import AIAnalysisResult, AnalysisHistory

class AIAnalysisResultSerializer(serializers.ModelSerializer):
    file_name = serializers.ReadOnlyField(source='file.filename')
    user_name = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = AIAnalysisResult
        fields = ['id', 'file', 'file_name', 'user', 'user_name', 'summary', 'extracted_info', 'status', 'version', 'created_at', 'updated_at', 'is_selected']
        read_only_fields = ['file', 'user', 'status', 'version', 'created_at', 'updated_at']

class AnalysisHistorySerializer(serializers.ModelSerializer):
    analysis_file = serializers.ReadOnlyField(source='analysis.file.filename')
    operator_name = serializers.ReadOnlyField(source='operator.username')
    
    class Meta:
        model = AnalysisHistory
        fields = ['id', 'analysis', 'analysis_file', 'action', 'action_time', 'operator', 'operator_name', 'details']
        read_only_fields = ['action_time']
