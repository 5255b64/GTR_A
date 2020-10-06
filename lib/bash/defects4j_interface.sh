#!/bin/bash

# 启动defects4j的接口脚本

# 第二个参数$1表示 DEFECTS4J_PRE_SOURCE_FILE_ADDR
# 第二个参数$2表示 defects4j的参数

# 添加环境变量
source $1
defects4j $2