<#
.SYNOPSIS
一键启动建设集团管理系统前端服务

.DESCRIPTION
自动完成依赖安装和前端开发服务器启动

.NOTES
Author: System Admin
Version: 1.0
Date: 2026-06-02
#>

# 设置颜色
$host.ui.RawUI.ForegroundColor = "Cyan"
Write-Host "`n==============================================="
Write-Host "       🏗️  建设集团管理系统 - 前端启动脚本"
Write-Host "==============================================="
$host.ui.RawUI.ForegroundColor = "Gray"

# 定义路径
$projectPath = $PWD.Path
$frontendPath = Join-Path $projectPath "frontend"

# 切换到前端目录
Write-Host "`n📂 切换到前端目录..."
Set-Location $frontendPath

# 检查Node.js
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js 版本: $nodeVersion"
} catch {
    $host.ui.RawUI.ForegroundColor = "Red"
    Write-Error "❌ Node.js 未安装或未配置环境变量！"
    exit 1
}

# 安装依赖
if (-not (Test-Path "node_modules")) {
    Write-Host "`n📦 安装依赖..."
    npm install
    
    if ($LASTEXITCODE -ne 0) {
        $host.ui.RawUI.ForegroundColor = "Red"
        Write-Error "❌ 依赖安装失败！"
        exit 1
    }
    Write-Host "✅ 依赖安装完成"
} else {
    Write-Host "`n📦 依赖已存在，跳过安装"
}

# 启动服务
$host.ui.RawUI.ForegroundColor = "Green"
Write-Host "`n🚀 启动前端服务..."
Write-Host "------------------------------------------------"
Write-Host "  服务地址: http://localhost:8084"
Write-Host "  登录页面: http://localhost:8084/login"
Write-Host "  仪表盘: http://localhost:8084/"
Write-Host "------------------------------------------------"
$host.ui.RawUI.ForegroundColor = "White"

npm run dev -- --host 0.0.0.0 --port 8084
