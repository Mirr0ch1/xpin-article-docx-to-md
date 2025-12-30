#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XPIN Article DOCX to MD Converter
主程序入口

这是一个用于将Word文档(.docx)转换为Markdown(.md)格式的工具。
遵循特定的转换规则：只保留标题和加粗格式，跳过图片，删除指定的开始内容。

使用方法:
    python main.py input_directory [output_directory]
    
参数:
    input_directory: 包含要转换的Word文档的目录
    output_directory: 可选的输出目录（默认为input_directory/markdown_files）
    
示例:
    python main.py ./documents
    python main.py ./documents ./output
"""

import sys
import argparse
from pathlib import Path
from converter import DocxToMdConverter
from config import Config
from utils import Logger, FileUtils, get_file_info
import json

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='XPIN Article DOCX to MD Converter - Word文档转Markdown工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s ./documents                    # 转换documents目录下的所有Word文档
  %(prog)s ./documents ./output          # 指定输出目录
  %(prog)s ./documents --no-recursive    # 不递归搜索子目录
  %(prog)s ./documents --dry-run         # 预览模式，不实际转换
        """
    )
    
    parser.add_argument(
        'input_dir',
        help='包含要转换的Word文档的目录'
    )
    
    parser.add_argument(
        'output_dir',
        nargs='?',
        help='输出目录（可选，默认为input_dir/markdown_files）'
    )
    
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='不递归搜索子目录'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式，显示将要转换的文件但不实际转换'
    )
    
    parser.add_argument(
        '--list-files',
        action='store_true',
        help='列出将要转换的文件'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细输出'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # 验证输入目录
    input_path = Path(args.input_dir)
    if not input_path.exists():
        Logger.error(f"输入目录不存在: {input_path}")
        sys.exit(1)
    
    if not input_path.is_dir():
        Logger.error(f"输入路径不是目录: {input_path}")
        sys.exit(1)
    
    # 查找文件
    if args.no_recursive:
        docx_files = [str(f) for f in input_path.iterdir() 
                     if f.is_file() and Config.is_supported_file(f)]
    else:
        docx_files = FileUtils.find_docx_files(input_path)
    
    if not docx_files:
        Logger.warning(f"在目录 {input_path} 中未找到支持的Word文档文件")
        sys.exit(0)
    
    # 列出文件（如果需要）
    if args.list_files:
        Logger.info(f"找到 {len(docx_files)} 个Word文档:")
        for i, file_path in enumerate(docx_files, 1):
            file_info = get_file_info(file_path)
            print(f"  {i:2d}. {file_info['name']} ({file_info['size']})")
        print()
    
    # 预览模式
    if args.dry_run:
        Logger.info("预览模式 - 以下文件将被转换:")
        for file_path in docx_files:
            output_path = Config.get_output_path(file_path, args.output_dir)
            print(f"  {file_path} -> {output_path}")
        return
    
    # 初始化转换器
    converter = DocxToMdConverter()
    
    # 执行转换
    Logger.info(f"开始转换 {len(docx_files)} 个Word文档...")
    
    try:
        results = converter.batch_convert(
            input_path, 
            args.output_dir, 
            recursive=not args.no_recursive
        )
        
        # 显示结果
        summary = converter.get_conversion_summary(results)
        
        print()  # 空行
        Logger.info("=" * 50)
        Logger.info("转换摘要:")
        Logger.info(f"  总文件数: {summary['total_files']}")
        Logger.info(f"  成功转换: {summary['successful_conversions']}")
        Logger.info(f"  转换失败: {summary['failed_conversions']}")
        Logger.info(f"  成功率: {summary['success_rate']:.1f}%")
        
        if args.verbose and summary['failed_conversions'] > 0:
            print()
            Logger.error("失败的转换:")
            for result in results:
                if not result['success']:
                    print(f"  ❌ {result['input_file']}: {result['error']}")
        
        # 显示输出目录
        output_dir = args.output_dir or str(Config.get_output_dir(input_path))
        print()
        Logger.success(f"转换结果保存在: {output_dir}")
        
    except KeyboardInterrupt:
        Logger.warning("\n用户中断转换过程")
        sys.exit(1)
    except Exception as e:
        Logger.error(f"转换过程中发生错误: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def interactive_mode():
    """交互模式"""
    Logger.info("XPIN Article DOCX to MD Converter - 交互模式")
    Logger.info("输入 'quit' 或 'exit' 退出程序\n")
    
    converter = DocxToMdConverter()
    
    while True:
        try:
            # 获取输入目录
            input_dir = input("请输入包含Word文档的目录路径: ").strip()
            
            if input_dir.lower() in ['quit', 'exit', 'q', '退出']:
                Logger.info("感谢使用！")
                break
            
            if not input_dir:
                Logger.warning("请输入有效的目录路径")
                continue
            
            # 获取输出目录
            output_dir = input("请输入输出目录（回车使用默认）: ").strip()
            if not output_dir:
                output_dir = None
            
            # 确认转换
            print(f"\n目录: {input_dir}")
            print(f"输出: {output_dir or '默认目录'}")
            confirm = input("\n确认开始转换？(y/N): ").strip().lower()
            
            if confirm not in ['y', 'yes', '是', '确定']:
                Logger.info("转换已取消")
                continue
            
            # 执行转换
            converter.batch_convert(input_dir, output_dir)
            print("\n" + "="*50)
            
        except KeyboardInterrupt:
            Logger.info("\n\n感谢使用！")
            break
        except Exception as e:
            Logger.error(f"发生错误: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 无参数时启动交互模式
        interactive_mode()
    else:
        # 命令行模式
        main()
