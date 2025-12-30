"""
XPIN Article DOCX to MD Converter
核心文档转换器
"""

import os
import re
from pathlib import Path
from docx import Document
from docx.shared import Inches
from config import Config
from utils import Logger, TextProcessor, FileUtils

class DocxToMdConverter:
    """DOCX到Markdown转换器"""
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.config = Config()
    
    def convert_file(self, input_path, output_dir=None):
        """
        转换单个文件
        
        Args:
            input_path: 输入文件路径
            output_dir: 输出目录（可选）
        
        Returns:
            dict: 转换结果信息
        """
        try:
            # 验证输入文件
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"文件不存在: {input_path}")
            
            if not Config.is_supported_file(input_path):
                raise ValueError(f"不支持的文件格式: {input_path}")
            
            # 读取DOCX文档
            doc = Document(input_path)
            
            # 转换文档内容
            markdown_content = self._convert_document(doc)
            
            # 清理内容
            markdown_content = self._clean_content(markdown_content)
            
            # 生成输出路径
            output_path = Config.get_output_path(input_path, output_dir)
            
            # 确保输出目录存在
            FileUtils.ensure_directory(output_path.parent)
            
            # 写入文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return {
                'success': True,
                'input_file': input_path,
                'output_file': str(output_path),
                'content_length': len(markdown_content)
            }
            
        except Exception as e:
            Logger.error(f"转换文件失败 {input_path}: {str(e)}")
            return {
                'success': False,
                'input_file': input_path,
                'error': str(e)
            }
    
    def _convert_document(self, doc):
        """转换文档内容"""
        markdown_lines = []
        
        for element in doc.element.body:
            # 处理段落
            if element.tag.endswith('p'):
                paragraph = self._find_paragraph_by_element(doc, element)
                if paragraph:
                    markdown_line = self._convert_paragraph(paragraph)
                    if markdown_line:
                        markdown_lines.append(markdown_line)
            
            # 处理表格（可选，根据需求跳过）
            elif element.tag.endswith('tbl'):
                # 根据需求，我们跳过表格
                Logger.warning("跳过表格内容（根据配置）")
                continue
            
            # 处理图片（跳过）
            elif element.tag.endswith('drawing') or element.tag.endswith('pic'):
                Logger.info("跳过图片内容")
                continue
        
        return '\n'.join(markdown_lines)
    
    def _find_paragraph_by_element(self, doc, element):
        """通过元素查找对应的段落对象"""
        for paragraph in doc.paragraphs:
            if paragraph._element == element:
                return paragraph
        return None
    
    def _convert_paragraph(self, paragraph):
        """转换单个段落"""
        text = paragraph.text.strip()
        if not text:
            return ""
        
        # 检查是否是标题
        if paragraph.style.name.startswith('Heading'):
            level = self._get_heading_level(paragraph.style.name)
            return f"{'#' * level} {text}"
        
        # 处理加粗文本
        formatted_text = self._format_text_with_styles(paragraph)
        
        return formatted_text
    
    def _get_heading_level(self, style_name):
        """获取标题级别"""
        if 'Heading 1' in style_name:
            return 1
        elif 'Heading 2' in style_name:
            return 2
        elif 'Heading 3' in style_name:
            return 3
        elif 'Heading 4' in style_name:
            return 4
        elif 'Heading 5' in style_name:
            return 5
        elif 'Heading 6' in style_name:
            return 6
        else:
            return 1  # 默认一级标题
    
    def _format_text_with_styles(self, paragraph):
        """格式化带样式的文本"""
        text_parts = []
        current_text = ""
        
        for run in paragraph.runs:
            run_text = run.text
            
            # 处理加粗
            if run.bold:
                if current_text:
                    text_parts.append(current_text)
                    current_text = ""
                text_parts.append(f"**{run_text}**")
            else:
                current_text += run_text
        
        # 添加剩余文本
        if current_text:
            text_parts.append(current_text)
        
        return ''.join(text_parts)
    
    def _clean_content(self, content):
        """清理转换后的内容"""
        # 删除开头的指定模式
        content = self.text_processor.remove_unwanted_patterns(
            content, Config.REMOVE_PATTERNS
        )
        
        # 清理文本
        content = self.text_processor.clean_text(content)
        
        return content
    
    def batch_convert(self, input_directory, output_dir=None, recursive=True):
        """
        批量转换目录中的文件
        
        Args:
            input_directory: 输入目录
            output_dir: 输出目录（可选）
            recursive: 是否递归搜索子目录
        
        Returns:
            list: 转换结果列表
        """
        # 查找所有DOCX文件
        if recursive:
            docx_files = FileUtils.find_docx_files(input_directory)
        else:
            from pathlib import Path
            directory_path = Path(input_directory)
            docx_files = [str(f) for f in directory_path.iterdir() 
                         if f.is_file() and Config.is_supported_file(f)]
        
        if not docx_files:
            Logger.warning(f"在目录 {input_directory} 中未找到支持的文档文件")
            return []
        
        # 创建输出目录
        if output_dir is None:
            output_dir = Config.get_output_dir(input_directory)
        FileUtils.ensure_directory(output_dir)
        
        Logger.info(f"开始批量转换 {len(docx_files)} 个文件...")
        
        # 批量转换
        results = []
        for docx_file in docx_files:
            result = self.convert_file(docx_file, output_dir)
            results.append(result)
        
        # 统计结果
        success_count = sum(1 for r in results if r['success'])
        error_count = len(results) - success_count
        
        Logger.success(f"转换完成! 成功: {success_count}, 失败: {error_count}")
        
        return results
    
    def get_conversion_summary(self, results):
        """获取转换摘要"""
        total = len(results)
        success = sum(1 for r in results if r['success'])
        failed = total - success
        
        summary = {
            'total_files': total,
            'successful_conversions': success,
            'failed_conversions': failed,
            'success_rate': (success / total * 100) if total > 0 else 0
        }
        
        return summary
