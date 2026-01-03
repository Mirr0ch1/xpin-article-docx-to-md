# 快速使用指南

## 🚀 立即开始

### 📦 安装 uv（推荐）

uv 是一个极速的 Python 包管理工具：

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 Homebrew
brew install uv
```

### 🖥️ 使用 uv 运行

```bash
# 创建虚拟环境并安装依赖
uv venv
uv pip install -r requirements.txt

# 运行程序
uv run python main.py ./documents

# 运行测试
uv run python test.py
```

## 🍎 macOS 用户

macOS 系统 Python 3.12+ 需要使用 uv 或虚拟环境：

```bash
# 方式一：使用 uv（推荐，最简单）
uv run python main.py ./documents

# 方式二：激活虚拟环境后使用
source venv/bin/activate
python main.py ./documents
deactivate

# 方式三：直接使用虚拟环境中的 Python
./venv/bin/python main.py ./documents
```

## 🐧 Linux 用户

```bash
# 使用 uv（推荐）
uv run python main.py ./documents

# 或使用安装脚本
chmod +x install.sh
./install.sh
python main.py ./documents
```

## 🪟 Windows 用户

```bash
# 使用 uv（推荐）
uv venv
uv pip install -r requirements.txt
uv run python main.py ./documents

# 或直接使用 pip
pip install -r requirements.txt
python main.py ./documents
```

## 📝 转换规则（已内置进脚本，无需干预）

### ✅ 保留格式
- 标题 (# ## ### 等)
- 加粗文本 (**文本**)

### ❌ 跳过内容
- 图片
- 表格
- 页眉页脚
- 其他格式（斜体、下划线等）

### 🗑️ 删除内容
文档开头删除：
- `## 原文`
- `123`
- `123123`

## 🧪 测试
```bash
# 使用 uv（推荐）
uv run python test.py

# 或激活虚拟环境后使用
source venv/bin/activate
python test.py
deactivate
```

## 📁 输出
转换后的文件保存在 `markdown_files/` 目录中，文件名保持不变，扩展名改为 `.md`。

---
详细说明请查看 README.md
