# GitHub 托管指南

## 📋 准备工作

### 1. 创建GitHub仓库

1. 登录到 [GitHub](https://github.com)
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `xpin-article-docx-to-md` (或您喜欢的名字)
   - **Description**: "一个专业的Word文档转Markdown工具，严格按照指定规则进行转换"
   - **Visibility**: Public (公开) 或 Private (私有)
   - **⚠️ 不要勾选** "Add a README file"、"Add .gitignore"、"Choose a license"
   - 点击 "Create repository"

### 2. 记录仓库地址

创建完成后，GitHub会显示仓库地址，类似：
```
https://github.com/您的用户名/xpin-article-docx-to-md.git
```

## 🚀 本地项目推送步骤

### 步骤1：进入项目目录
```bash
cd /workspace/xpin-article-docx-to-md
```

### 步骤2：初始化Git仓库
```bash
git init
```

### 步骤3：配置用户信息（如果还没有配置）
```bash
git config --global user.name "您的姓名"
git config --global user.email "您的邮箱"
```

### 步骤4：添加.gitignore文件
创建 `.gitignore` 文件（可选，推荐）：
```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 虚拟环境
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 系统文件
.DS_Store
Thumbs.db
```

### 步骤5：添加文件到Git
```bash
git add .
```

### 步骤6：提交代码
```bash
git commit -m "Initial commit: 完整的Word转Markdown转换工具

✨ 功能特点:
- 精确转换规则：只保留标题和加粗格式
- 智能跳过：自动跳过图片和其他不支持内容
- 内容清理：自动删除指定开头内容
- 批量处理：支持目录级别批量转换
- 跨平台：Windows、macOS、Linux全支持
- 详细日志：提供转换进度和结果统计
- 测试覆盖：完整的单元测试确保质量

🧪 测试结果:
- 9个单元测试全部通过
- 支持交互模式和命令行模式
- 完善的错误处理和用户提示
"
```

### 步骤7：连接到远程仓库
将下面命令中的 `您的用户名` 替换为您的实际GitHub用户名：
```bash
git remote add origin https://github.com/您的用户名/xpin-article-docx-to-md.git
```

### 步骤8：推送到GitHub
```bash
git branch -M main
git push -u origin main
```

## ✅ 验证推送成功

1. 刷新GitHub页面
2. 应该能看到所有文件已上传
3. 点击仓库的 "Settings" -> "Pages" 可配置GitHub Pages

## 📝 推送到GitHub后的优化

### 1. 添加GitHub主题（可选）
在GitHub仓库页面：
1. 点击 "Add file" -> "Create new file"
2. 文件名输入：`README.md`
3. 内容会自动显示现有README文件的内容

### 2. 添加发布标签（可选）
```bash
git tag v1.0.0
git push origin v1.0.0
```

### 3. 添加许可证文件
在GitHub页面添加LICENSE文件，推荐使用MIT许可证。

## 🔧 常见问题解决

### Q1: 推送时被拒绝
如果出现 "Updates were rejected" 错误：
```bash
git pull origin main --rebase
git push origin main
```

### Q2: 证书验证失败
如果HTTPS推送失败，可以改用SSH：
```bash
git remote set-url origin git@github.com:您的用户名/xpin-article-docx-to-md.git
```

### Q3: 大文件推送失败
如果项目文件较大，可以使用Git LFS：
```bash
git lfs install
git lfs track "*.pyc"
git add .gitattributes
git add .
git commit -m "Add LFS tracking"
git push origin main
```

## 🎯 推送完成后的操作

1. **测试访问**: 确认GitHub仓库可以正常访问
2. **测试克隆**: 在另一个目录测试 `git clone` 功能
3. **分享项目**: 将仓库链接分享给其他人
4. **持续更新**: 以后可以直接 `git push` 推送更新

## 📚 推荐的后续步骤

1. **添加演示**: 可以录制一个使用演示视频
2. **完善文档**: 在README中添加更多使用示例
3. **收集反馈**: 鼓励用户提交Issue和反馈
4. **持续改进**: 根据用户反馈不断优化工具

---

## 🎊 恭喜！

您的项目现在已经成功托管到GitHub，可以：
- 与世界分享您的代码
- 获得社区反馈和改进建议
- 建立个人技术品牌
- 为其他开发者提供有用的工具

祝您使用愉快！🚀
