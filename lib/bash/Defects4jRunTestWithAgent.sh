#!/usr/bin/env bash
# 在使用agent的情况下
# 运行指定的testsuite（bz2压缩包形式）

# 第一个参数$1表示 DEFECTS4J_PRE_SOURCE_FILE_ADDR
# 第二个参数$2表示 DEFECTS4J_PRE_INCLUDE_FILE_ADDR

# 加载defects4j环境变量
source $1

# 加载.include文件
# source diy.include
source $2
init

working_directory=$3  # $3 checkout 路径
log_output_addr=$4  # $4 输入日志地址
testsuite_addr=$5   # $5 testsuite 路径
build_file=$6       # $6 build file

# test_diy
# echo defects4j -w $working_directory -o $log_output_addr -s $testsuite_addr -a $build_file
defects4j test_diy -w $working_directory -o $log_output_addr -s $testsuite_addr -a $build_file
