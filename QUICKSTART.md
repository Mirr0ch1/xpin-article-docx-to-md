# 快速使用指南

## 🚀 立即开始

### 📦 安装依赖

#### macOS（推荐）
```bash
chmod +x install_mac.sh
./install_mac.sh
```

#### Linux/macOS
```bash
chmod +x install.sh
./install.sh
```

#### Windows
```bash
pip install -r requirements.txt
```

### 🖥️ 基本使用

```bash
# 转换当前目录下的所有Word文档
python main.py ./documents

# 指定输出目录
python main.py ./documents ./output
```

### 🎮 交互模式
```bash
python main.py
```

## 🍎 macOS 用户

macOS 系统 Python 3.12+ 需要使用虚拟环境：

```bash
# 方式一：激活虚拟环境后使用
source venv/bin/activate
python main.py ./documents
deactivate

# 方式二：直接使用虚拟环境中的 Python
./venv/bin/python main.py ./documents
```

## 📝 转换规则

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
# Linux/macOS
python test.py

# macOS
source venv/bin/activate
python test.py
deactivate
```

## 📁 输出
转换后的文件保存在 `markdown_files/` 目录中，文件名保持不变，扩展名改为 `.md`。

---
详细说明请查看 README.md
