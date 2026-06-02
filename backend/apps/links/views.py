from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
import json

def links_page(request):
    links = {
        '前端页面': [
            {'name': '登录页面', 'url': 'http://localhost:8084/login', 'description': '用户登录界面'},
            {'name': '仪表盘', 'url': 'http://localhost:8084/', 'description': '系统首页/数据统计'},
            {'name': '文件管理', 'url': 'http://localhost:8084/files', 'description': '文件上传、下载、分类'},
            {'name': 'AI分析', 'url': 'http://localhost:8084/ai-analysis', 'description': '文档AI分析功能'},
            {'name': '用户管理', 'url': 'http://localhost:8084/users', 'description': '用户CRUD（管理员权限）'},
        ],
        '后端API': [
            {'name': '用户登录', 'url': '/api/auth/login/', 'method': 'POST', 'description': '用户名密码登录，返回token'},
            {'name': '用户注册', 'url': '/api/auth/register/', 'method': 'POST', 'description': '新用户注册'},
            {'name': '用户列表', 'url': '/api/auth/users/', 'method': 'GET', 'description': '获取用户列表（管理员）'},
            {'name': '文件列表', 'url': '/api/files/files/', 'method': 'GET', 'description': '获取文件列表'},
            {'name': '文件上传', 'url': '/api/files/files/', 'method': 'POST', 'description': '上传文件（multipart/form-data）'},
            {'name': '文件分类', 'url': '/api/files/categories/', 'method': 'GET/POST', 'description': '文件分类管理'},
            {'name': 'AI分析', 'url': '/api/ai/results/analyze/', 'method': 'POST', 'description': '对文件进行AI分析'},
            {'name': '分析结果', 'url': '/api/ai/results/', 'method': 'GET', 'description': '获取分析结果列表'},
            {'name': '分析历史', 'url': '/api/ai/history/', 'method': 'GET', 'description': '分析历史记录'},
        ],
        '管理后台': [
            {'name': 'Django管理', 'url': '/admin/', 'description': 'Django内置管理后台'},
            {'name': 'RabbitMQ管理', 'url': 'http://localhost:15672/', 'description': 'RabbitMQ消息队列管理（guest/guest）'},
        ],
        '测试账号': [
            {'name': '管理员', 'username': 'admin', 'password': 'admin', 'role': 'admin', 'phone': '13800138000'},
        ]
    }

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>建设集团管理系统 - 链接导航</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 40px 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { text-align: center; color: white; margin-bottom: 40px; font-size: 2.5rem; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }
        .section { background: white; border-radius: 12px; padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); }
        .section h2 { color: #333; margin-bottom: 20px; font-size: 1.4rem; border-left: 4px solid #667eea; padding-left: 15px; }
        .link-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }
        .link-item { background: #f8f9fa; border-radius: 8px; padding: 20px; transition: all 0.3s ease; border: 1px solid #e9ecef; }
        .link-item:hover { transform: translateY(-3px); box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
        .link-item .name { font-weight: 600; color: #333; margin-bottom: 8px; font-size: 1.1rem; }
        .link-item .url { font-family: monospace; font-size: 0.9rem; color: #667eea; word-break: break-all; margin-bottom: 8px; }
        .link-item .url a { color: #667eea; text-decoration: none; }
        .link-item .url a:hover { text-decoration: underline; }
        .link-item .method { display: inline-block; background: #667eea; color: white; padding: 3px 10px; border-radius: 4px; font-size: 0.8rem; margin-right: 10px; }
        .link-item .method.get { background: #28a745; }
        .link-item .method.post { background: #667eea; }
        .link-item .method.put { background: #ffc107; color: #333; }
        .link-item .method.delete { background: #dc3545; }
        .link-item .desc { color: #666; font-size: 0.9rem; }
        .account-table { width: 100%; border-collapse: collapse; }
        .account-table th, .account-table td { padding: 12px; text-align: left; border-bottom: 1px solid #e9ecef; }
        .account-table th { background: #f8f9fa; font-weight: 600; color: #333; }
        .account-table tr:hover { background: #f8f9fa; }
        .server-status { display: flex; gap: 20px; margin-bottom: 20px; }
        .status-item { display: flex; align-items: center; gap: 10px; }
        .status-dot { width: 12px; height: 12px; border-radius: 50%; background: #28a745; }
        .status-dot.offline { background: #dc3545; }
        .status-text { color: #333; font-weight: 500; }
        .header { text-align: center; margin-bottom: 30px; }
        .header p { color: rgba(255,255,255,0.9); font-size: 1.1rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏗️ 建设集团管理系统</h1>
            <p>API链接导航与测试页面</p>
        </div>

        <div class="section">
            <h2>📊 服务状态</h2>
            <div class="server-status">
                <div class="status-item"><div class="status-dot"></div><span class="status-text">后端服务: 运行中 (http://localhost:8000)</span></div>
                <div class="status-item"><div class="status-dot"></div><span class="status-text">前端服务: 运行中 (http://localhost:8084)</span></div>
                <div class="status-item"><div class="status-dot"></div><span class="status-text">RabbitMQ: 运行中 (http://localhost:15672)</span></div>
            </div>
        </div>

        <div class="section">
            <h2>🌐 前端页面</h2>
            <div class="link-list">
"""

    for link in links['前端页面']:
        html += f"""
                <div class="link-item">
                    <div class="name">🔗 {link['name']}</div>
                    <div class="url"><a href="{link['url']}" target="_blank">{link['url']}</a></div>
                    <div class="desc">📝 {link['description']}</div>
                </div>"""

    html += """
            </div>
        </div>

        <div class="section">
            <h2>🔌 后端API接口</h2>
            <div class="link-list">
"""

    for link in links['后端API']:
        method_class = link.get('method', 'GET').lower().split('/')[0]
        html += f"""
                <div class="link-item">
                    <div class="name">🔗 {link['name']}</div>
                    <div class="url">
                        <span class="method {method_class}">{link.get('method', 'GET')}</span>
                        <a href="http://localhost:8000{link['url']}" target="_blank">http://localhost:8000{link['url']}</a>
                    </div>
                    <div class="desc">📝 {link['description']}</div>
                </div>"""

    html += """
            </div>
        </div>

        <div class="section">
            <h2>⚙️ 管理后台</h2>
            <div class="link-list">
"""

    for link in links['管理后台']:
        html += f"""
                <div class="link-item">
                    <div class="name">🔗 {link['name']}</div>
                    <div class="url"><a href="{link['url']}" target="_blank">{link['url']}</a></div>
                    <div class="desc">📝 {link['description']}</div>
                </div>"""

    html += """
            </div>
        </div>

        <div class="section">
            <h2>👤 测试账号</h2>
            <table class="account-table">
                <tr><th>角色</th><th>用户名</th><th>密码</th><th>联系电话</th></tr>
"""

    for account in links['测试账号']:
        html += f"""
                <tr>
                    <td>{account['role']}</td>
                    <td>{account['username']}</td>
                    <td>{account['password']}</td>
                    <td>{account['phone']}</td>
                </tr>"""

    html += """
            </table>
        </div>

        <div class="section">
            <h2>📖 API测试示例</h2>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; font-family: monospace; font-size: 0.9rem; line-height: 1.6;">
                <strong>登录请求:</strong><br>
                POST http://localhost:8000/api/auth/login/<br>
                Content-Type: application/json<br>
                Body: {"username": "admin", "password": "admin"}<br><br>

                <strong>文件上传:</strong><br>
                POST http://localhost:8000/api/files/files/<br>
                Content-Type: multipart/form-data<br>
                Body: file=[文件], category=[分类ID], description=[描述]<br><br>

                <strong>AI分析:</strong><br>
                POST http://localhost:8000/api/ai/results/analyze/<br>
                Content-Type: application/json<br>
                Headers: Authorization: Token [token]<br>
                Body: {"file_id": 1}
            </div>
        </div>

        <div style="text-align: center; color: rgba(255,255,255,0.8); margin-top: 40px; font-size: 0.9rem;">
            建设集团管理系统 v1.0 | 最后更新: 2026-06-02
        </div>
    </div>
</body>
</html>
"""
    return HttpResponse(html)
