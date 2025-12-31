#!/bin/bash
# XPIN Article DOCX to MD Converter
# macOS 专用安装脚本（使用虚拟环境）

echo "========================================"
echo "XPIN Article DOCX to MD Converter"
echo "macOS 安装脚本"
echo "========================================"
echo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "[信息] 检查Python环境..."

if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python 3"
    echo "请先安装Python 3: brew install python3"
    exit 1
fi

echo "[信息] 检测到Python 3"

if [ -d "$VENV_DIR" ]; then
    echo "[信息] 检测到已存在的虚拟环境"
    read -p "是否重新创建? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "[信息] 删除旧虚拟环境..."
        rm -rf "$VENV_DIR"
    fi
fi

if [ ! -d "$VENV_DIR" ]; then
    echo
    echo "[步骤 1/4] 创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "[错误] 创建虚拟环境失败"
        exit 1
    fi
    echo "[信息] 虚拟环境创建成功: $VENV_DIR"
fi

echo
echo "[步骤 2/4] 激活虚拟环境并安装依赖包..."
source "$VENV_DIR/bin/activate"

if ! pip install -r "$SCRIPT_DIR/requirements.txt"; then
    echo "[错误] 依赖包安装失败"
    deactivate
    exit 1
fi

deactivate

echo
echo "[步骤 3/4] 运行测试..."
source "$VENV_DIR/bin/activate"
python "$SCRIPT_DIR/test.py"
TEST_RESULT=$?
deactivate

if [ $TEST_RESULT -ne 0 ]; then
    echo "[警告] 测试执行有问题，但继续安装"
fi

echo
echo "[步骤 4/4] 创建示例测试文件..."
source "$VENV_DIR/bin/activate"
python "$SCRIPT_DIR/test.py" --sample
deactivate

echo
echo "========================================"
echo "安装完成！"
echo "========================================"
echo
echo "使用方法:"
echo "  1. 先激活虚拟环境: source venv/bin/activate"
echo "  2. 运行程序: python main.py <输入目录> [输出目录]"
echo "  3. 退出虚拟环境: deactivate"
echo
echo "或者直接使用虚拟环境中的Python:"
echo "  ./venv/bin/python main.py <输入目录> [输出目录]"
echo
echo "交互模式:"
echo "  ./venv/bin/python main.py"
echo
echo "详细说明请查看 README.md 文件"
echo
