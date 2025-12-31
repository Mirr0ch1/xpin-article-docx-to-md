#!/bin/bash
# XPIN Article DOCX to MD Converter
# Linux/macOS 安装脚本

echo "========================================"
echo "XPIN Article DOCX to MD Converter"
echo "Linux/macOS 安装脚本"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "[错误] 未检测到Python，请先安装Python 3.6+"
        echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "macOS: brew install python3"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "[信息] 检测到Python，开始安装依赖包..."
echo

# 安装依赖包
echo "[步骤 1/3] 安装Python依赖包..."
if ! $PYTHON_CMD -m pip install -r requirements.txt; then
    echo "[错误] 依赖包安装失败"
    exit 1
fi

echo
echo "[步骤 2/3] 运行测试..."
if ! $PYTHON_CMD test.py; then
    echo "[警告] 测试执行有问题，但继续安装"
fi

echo
echo "[步骤 3/3] 创建示例测试文件..."
$PYTHON_CMD test.py --sample

echo
echo "========================================"
echo "安装完成！"
echo "========================================"
echo
echo "使用方法:"
echo "  $PYTHON_CMD main.py <输入目录> [输出目录]"
echo
echo "示例:"
echo "  $PYTHON_CMD main.py ./documents"
echo "  $PYTHON_CMD main.py ./documents ./output"
echo
echo "交互模式:"
echo "  $PYTHON_CMD main.py"
echo
echo "详细说明请查看 README.md 文件"
echo
