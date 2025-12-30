@echo off
REM XPIN Article DOCX to MD Converter
REM Windows 安装脚本

echo ========================================
echo XPIN Article DOCX to MD Converter
echo Windows 安装脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装Python 3.6+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [信息] 检测到Python，开始安装依赖包...
echo.

REM 安装依赖包
echo [步骤 1/3] 安装Python依赖包...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [错误] 依赖包安装失败
    pause
    exit /b 1
)

echo.
echo [步骤 2/3] 运行测试...
python test.py

echo.
echo [步骤 3/3] 创建示例测试文件...
python test.py --sample

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 使用方法:
echo   python main.py ^<输入目录^> [输出目录]
echo.
echo 示例:
echo   python main.py ./documents
echo   python main.py ./documents ./output
echo.
echo 交互模式:
echo   python main.py
echo.
echo 详细说明请查看 README.md 文件
echo.
pause
