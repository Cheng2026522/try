from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AIAnalysisResult, AnalysisHistory
from .serializers import AIAnalysisResultSerializer, AnalysisHistorySerializer
from apps.file_management.models import UploadedFile
from django.db.models import Max
import time

class AIAnalysisResultViewSet(viewsets.ModelViewSet):
    queryset = AIAnalysisResult.objects.all()
    serializer_class = AIAnalysisResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = AIAnalysisResult.objects.all()
        user = self.request.user
        if not user.is_superuser and user.role != 'admin':
            queryset = queryset.filter(user=user)
        return queryset
    
    @action(detail=False, methods=['post'])
    def analyze(self, request):
        file_id = request.data.get('file_id')
        try:
            uploaded_file = UploadedFile.objects.get(pk=file_id)
            if not request.user.is_superuser and uploaded_file.user != request.user:
                return Response({'detail': '无权分析此文件'}, status=status.HTTP_403_FORBIDDEN)
            
            max_version = AIAnalysisResult.objects.filter(file=uploaded_file).aggregate(Max('version'))['version__max']
            new_version = max_version + 1 if max_version else 1
            
            analysis = AIAnalysisResult.objects.create(
                file=uploaded_file,
                user=request.user,
                version=new_version,
                status='processing'
            )
            
            AnalysisHistory.objects.create(
                analysis=analysis,
                action='开始分析',
                operator=request.user,
                details={'file_id': file_id, 'version': new_version}
            )
            
            time.sleep(2)
            
            mock_summary = f"这是对文件'{uploaded_file.filename}'的AI分析摘要。该文件类型为{uploaded_file.file_type}，文件大小约{uploaded_file.size / 1024:.2f}KB。\n\n分析要点：\n1. 文件内容已成功解析\n2. 关键信息已提取\n3. 生成了结构化的分析报告"
            
            mock_extracted_info = {
                "file_name": uploaded_file.filename,
                "file_type": uploaded_file.file_type,
                "file_size": uploaded_file.size,
                "upload_time": uploaded_file.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
                "key_points": [
                    {"name": "项目名称", "value": "建设工程项目"},
                    {"name": "合同金额", "value": "1000万元"},
                    {"name": "项目周期", "value": "2024年1月-2024年12月"},
                    {"name": "参与单位", "value": "建设集团有限公司"},
                    {"name": "负责人", "value": "张三"},
                ],
                "analysis_date": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            analysis.summary = mock_summary
            analysis.extracted_info = mock_extracted_info
            analysis.status = 'completed'
            analysis.save()
            
            uploaded_file.is_analyzed = True
            uploaded_file.save()
            
            AnalysisHistory.objects.create(
                analysis=analysis,
                action='分析完成',
                operator=request.user,
                details={'summary_generated': True, 'info_extracted': True}
            )
            
            return Response({
                'detail': '分析完成', 
                'analysis_id': analysis.id,
                'summary': mock_summary,
                'extracted_info': mock_extracted_info
            }, status=status.HTTP_200_OK)
        except UploadedFile.DoesNotExist:
            return Response({'detail': '文件不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def qa(self, request, pk=None):
        analysis = self.get_object()
        question = request.data.get('question')
        
        if not question:
            return Response({'detail': '请提供问题'}, status=status.HTTP_400_BAD_REQUEST)
        
        mock_answer = f"基于文档分析，关于'{question}'的回答：这是一个模拟的智能问答响应。文档摘要：{analysis.summary[:100]}..."
        
        AnalysisHistory.objects.create(
            analysis=analysis,
            action='智能问答',
            operator=request.user,
            details={'question': question, 'answer': mock_answer}
        )
        
        return Response({'answer': mock_answer}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def update_result(self, request, pk=None):
        analysis = self.get_object()
        summary = request.data.get('summary')
        extracted_info = request.data.get('extracted_info')
        
        if summary:
            analysis.summary = summary
        if extracted_info:
            analysis.extracted_info = extracted_info
        analysis.status = 'completed'
        analysis.save()
        
        AnalysisHistory.objects.create(
            analysis=analysis,
            action='更新分析结果',
            operator=request.user,
            details={'summary_updated': bool(summary), 'info_updated': bool(extracted_info)}
        )
        
        return Response({'detail': '分析结果已更新'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def select_version(self, request, pk=None):
        analysis = self.get_object()
        AIAnalysisResult.objects.filter(file=analysis.file).update(is_selected=False)
        analysis.is_selected = True
        analysis.save()
        
        AnalysisHistory.objects.create(
            analysis=analysis,
            action='选择版本',
            operator=request.user,
            details={'version': analysis.version}
        )
        
        return Response({'detail': '已选择此版本'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_selected_version(self, request):
        file_id = request.query_params.get('file_id')
        if not file_id:
            return Response({'detail': '请提供file_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            analysis = AIAnalysisResult.objects.get(file_id=file_id, is_selected=True)
            return Response(AIAnalysisResultSerializer(analysis).data)
        except AIAnalysisResult.DoesNotExist:
            return Response({'detail': '未找到选中的版本'}, status=status.HTTP_404_NOT_FOUND)

class AnalysisHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AnalysisHistory.objects.all()
    serializer_class = AnalysisHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = AnalysisHistory.objects.all()
        user = self.request.user
        if not user.is_superuser and user.role != 'admin':
            queryset = queryset.filter(operator=user)
        return queryset
