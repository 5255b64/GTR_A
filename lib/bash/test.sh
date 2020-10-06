#!/bin/bash

echo "测试脚本 启动defects4j"

# 第一个参数$1表示 MAIN_FOLDER_ARRD
# 第二个参数$2表示 PRE_SOURCE_FILE_ADDR
echo bash hello
echo "执行的文件名：$0"
echo "第一个参数为：$1"
echo "第二个参数为：$2"

# 添加环境变量
source $2
defects4j

