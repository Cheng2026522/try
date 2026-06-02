<#
.SYNOPSIS
一键启动建设集团管理系统后端服务

.DESCRIPTION
自动完成虚拟环境激活、依赖安装、数据库迁移和服务启动

.NOTES
Author: System Admin
Version: 1.0
Date: 2026-06-02
#>

# 设置颜色
$host.ui.RawUI.ForegroundColor = "Cyan"
Write-Host "`n==============================================="
Write-Host "       🏗️  建设集团管理系统 - 后端启动脚本"
Write-Host "==============================================="
$host.ui.RawUI.ForegroundColor = "Gray"

# 定义路径
$projectPath = $PWD.Path
$backendPath = Join-Path $projectPath "backend"
$venvPath = Join-Path $backendPath "Group_env"
$venvActivate = Join-Path $venvPath "Scripts\Activate.ps1"

# 切换到后端目录
Write-Host "`n📂 切换到后端目录..."
Set-Location $backendPath

# 检查虚拟环境
if (-not (Test-Path $venvPath)) {
    $host.ui.RawUI.ForegroundColor = "Yellow"
    Write-Host "⚠️  虚拟环境不存在，正在创建..."
    $host.ui.RawUI.ForegroundColor = "Gray"
    
    python -m venv Group_env
    
    if (-not (Test-Path $venvActivate)) {
        $host.ui.RawUI.ForegroundColor = "Red"
        Write-Error "❌ 虚拟环境创建失败！"
        exit 1
    }
    Write-Host "✅ 虚拟环境创建成功"
}

# 激活虚拟环境
Write-Host "`n🔧 激活虚拟环境..."
& $venvActivate

# 安装依赖
Write-Host "`n📦 安装/更新依赖..."
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    $host.ui.RawUI.ForegroundColor = "Red"
    Write-Error "❌ 依赖安装失败！"
    exit 1
}
Write-Host "✅ 依赖安装完成"

# 数据库迁移
Write-Host "`n🗄️  执行数据库迁移..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

if ($LASTEXITCODE -ne 0) {
    $host.ui.RawUI.ForegroundColor = "Red"
    Write-Error "❌ 数据库迁移失败！"
    exit 1
}
Write-Host "✅ 数据库迁移完成"

# 启动服务
$host.ui.RawUI.ForegroundColor = "Green"
Write-Host "`n🚀 启动后端服务..."
Write-Host "------------------------------------------------"
Write-Host "  服务地址: http://localhost:8000"
Write-Host "  管理后台: http://localhost:8000/admin/"
Write-Host "  链接导航: http://localhost:8000/"
Write-Host "------------------------------------------------"
$host.ui.RawUI.ForegroundColor = "White"

python manage.py runserver 0.0.0.0:8000
