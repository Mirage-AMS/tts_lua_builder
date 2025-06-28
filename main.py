# ----------------------------------------
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @author       : 
# @email        : 
# @time         : 2025/6/23 14:18
# @file         : main.py
# @Desc         :
# -----------------------------------------

# import from official
import argparse
import os
import re
from pathlib import Path
# import from third-party

# import from self-defined
from src.build_lua_script import LuaBuilder


def main():
    # 创建解析器
    arg_parser = argparse.ArgumentParser(description="Build lua script")

    # 添加命令行参数
    arg_parser.add_argument("--input_dir", "-i", type=str, required=True, help="target input directory of the Lua project")
    arg_parser.add_argument("--output_file", "-o", type=str, required=True, help="target output file for the merged Lua script")
    arg_parser.add_argument("--verbose", "-v", action="store_true", help="enable verbose output for detailed information")
    arg_parser.add_argument("--mock", "-m", action="store_true", help="use mock data for compilation")

    # 解析命令行参数
    args = arg_parser.parse_args()

    # 调用build_lua_script函数
    LuaBuilder(args.input_dir, args.output_file, args.verbose, args.mock).run()


if __name__ == "__main__":
    main()