@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist node_modules\three\package.json (
  call npm.cmd ci --no-audit --no-fund
  if errorlevel 1 (
    echo 预览依赖安装失败，请检查网络和 Node.js。
    pause
    exit /b 1
  )
)
echo 请在浏览器打开 http://127.0.0.1:8766/
echo 保持此窗口开启。按 Ctrl+C 可停止本地预览。
python ..\scripts\serve_preview.py
pause
