"""
XPIN Article DOCX to MD Converter
工具函数模块
"""

import os
import re
from pathlib import Path
from colorama import Fore, Back, Style, init

# 初始化colorama
init(autoreset=True)

class Logger:
    """日志输出类"""
    
    @staticmethod
    def info(message):
        """信息日志"""
        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def success(message):
        """成功日志"""
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def warning(message):
        """警告日志"""
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def error(message):
        """错误日志"""
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def progress(current, total, filename):
        """进度显示"""
        percentage = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        print(f"\r{Fore.CYAN}[PROGRESS]{Style.RESET_ALL} [{bar}] {percentage:.1f}% - {filename}", end="", flush=True)

class FileUtils:
    """文件操作工具类"""
    
    @staticmethod
    def ensure_directory(path):
        """确保目录存在"""
        Path(path).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def find_docx_files(directory):
        """递归查找目录中的所有docx文件"""
        from config import Config
        files = []
        directory_path = Path(directory)
        
        if not directory_path.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")
        
        for file_path in directory_path.rglob('*'):
            if file_path.is_file() and Config.is_supported_file(file_path):
                files.append(str(file_path))
        
        return sorted(files)
    
    @staticmethod
    def safe_filename(filename):
        """生成安全的文件名"""
        # 移除或替换不安全的字符
        unsafe_chars = '<>:"/\\|?*'
        safe_name = filename
        for char in unsafe_chars:
            safe_name = safe_name.replace(char, '_')
        return safe_name

class TextProcessor:
    """文本处理工具类"""
    
    @staticmethod
    def remove_unwanted_patterns(text, patterns):
        """删除文本开头的指定模式"""
        lines = text.split('\n')
        
        # 查找要删除的行
        lines_to_remove = []
        for i, line in enumerate(lines):
            for pattern in patterns:
                if re.match(pattern, line.strip()):
                    lines_to_remove.append(i)
                    break
        
        # 删除这些行
        for index in reversed(lines_to_remove):
            del lines[index]
        
        return '\n'.join(lines)
    
    @staticmethod
    def clean_text(text):
        """清理文本"""
        # 移除多余的空行
        lines = text.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            stripped = line.strip()
            if stripped == '':
                if not prev_empty:
                    cleaned_lines.append('')
                prev_empty = True
            else:
                cleaned_lines.append(line)
                prev_empty = False
        
        return '\n'.join(cleaned_lines)
    
    @staticmethod
    def format_paragraph(paragraph):
        """格式化段落"""
        text = paragraph.text.strip()
        if not text:
            return ""
        
        # 处理粗体
        for run in paragraph.runs:
            if run.bold:
                text = text.replace(run.text, f"**{run.text}**")
        
        return text

class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self, total):
        self.total = total
        self.current = 0
    
    def update(self, filename):
        """更新进度"""
        self.current += 1
        Logger.progress(self.current, self.total, filename)
        
        if self.current == self.total:
            print()  # 换行
    
    def reset(self):
        """重置进度"""
        self.current = 0

def format_file_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def get_file_info(file_path):
    """获取文件信息"""
    path = Path(file_path)
    return {
        'name': path.name,
        'size': format_file_size(path.stat().st_size),
        'extension': path.suffix.lower()
    }
