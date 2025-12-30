"""
XPIN Article DOCX to MD Converter
配置文件
"""

import os
from pathlib import Path

class Config:
    """程序配置类"""
    
    # 支持的文件扩展名
    SUPPORTED_EXTENSIONS = {'.docx', '.doc'}
    
    # 输出扩展名
    OUTPUT_EXTENSION = '.md'
    
    # 需要删除的开头内容模式
    REMOVE_PATTERNS = [
        r'^## 原文\s*$',  # 删除 "## 原文"
        r'^123\s*$',      # 删除 "123"
        r'^123123\s*$',   # 删除 "123123"
    ]
    
    # 保留的文本格式
    PRESERVED_FORMATS = {
        'bold': '**',      # 粗体用 ** 包围
        'italic': '*',     # 斜体用 * 包围
        'heading': '#',    # 标题用 # 前缀
    }
    
    # 跳过的内容类型
    SKIP_CONTENT_TYPES = [
        'PICTURE',         # 图片
        'TABLE',           # 表格（根据需求）
        'HEADER',          # 页眉
        'FOOTER',          # 页脚
    ]
    
    # 输出目录名称
    OUTPUT_DIR_NAME = 'markdown_files'
    
    # 配置文件路径
    CONFIG_FILE = 'config.ini'
    
    @classmethod
    def get_output_dir(cls, input_dir):
        """获取输出目录路径"""
        input_path = Path(input_dir)
        output_path = input_path.parent / cls.OUTPUT_DIR_NAME
        return output_path
    
    @classmethod
    def is_supported_file(cls, file_path):
        """检查是否为支持的文档格式"""
        return Path(file_path).suffix.lower() in cls.SUPPORTED_EXTENSIONS
    
    @classmethod
    def get_output_path(cls, input_path, output_dir=None):
        """获取输出文件路径"""
        input_file = Path(input_path)
        if output_dir is None:
            output_dir = cls.get_output_dir(str(input_file.parent))
        else:
            output_dir = Path(output_dir)
        
        # 保持原文件名，替换扩展名
        output_file = output_dir / f"{input_file.stem}{cls.OUTPUT_EXTENSION}"
        return output_file
