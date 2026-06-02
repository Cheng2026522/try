from celery import shared_task
from .models import AIAnalysisResult, AnalysisHistory
from apps.file_management.models import UploadedFile
import time
import docx
import json

@shared_task
def analyze_file_task(analysis_id):
    try:
        analysis = AIAnalysisResult.objects.get(pk=analysis_id)
        uploaded_file = analysis.file
        
        time.sleep(3)
        
        mock_summary = f"这是对文件'{uploaded_file.filename}'的AI分析摘要。该文件类型为{uploaded_file.get_file_type_display()}，文件大小约{uploaded_file.size / 1024:.2f}KB。\n\n分析要点：\n1. 文件内容已成功解析\n2. 关键信息已提取\n3. 生成了结构化的分析报告"
        
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
            operator=analysis.user,
            details={'summary_generated': True, 'info_extracted': True}
        )
        
    except AIAnalysisResult.DoesNotExist:
        pass
    except Exception as e:
        try:
            analysis = AIAnalysisResult.objects.get(pk=analysis_id)
            analysis.status = 'failed'
            analysis.save()
            AnalysisHistory.objects.create(
                analysis=analysis,
                action='分析失败',
                operator=analysis.user,
                details={'error': str(e)}
            )
        except:
            pass
