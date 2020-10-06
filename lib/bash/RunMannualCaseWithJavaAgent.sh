#!/usr/bin/env bash

# 第一个参数$1表示 DEFECTS4J_PRE_SOURCE_FILE_ADDR
# 第二个参数$2表示 checkout的存储路径
# 第3个参数$3表示  -o ant日志输出路径
# 第4个参数$4表示  -a ant_build_file_addr 路径
# 第5个参数$5表示  project_id
# 第6个参数$6表示  version_num
# 第7个参数$7表示  bf_type
# 第8个参数$8表示

# 加载defects4j环境变量
# export DEFECT4J_PATH=/home/gx/Code/TestMinimization/defects4j-master
source $1

checkout_addr=$2
ant_log_output=$3
ant_build_file_addr=$4
project_id=$5
version_num=$6
bf_type=$7

#echo checkout_addr=$checkout_addr
#echo ant_log_output=$ant_log_output
#echo ant_build_file_addr=$ant_build_file_addr
#echo project_id=$project_id
#echo version_num=$version_num
#echo bf_type=$bf_type

# 生成checkout
echo defects4j checkout -p $project_id -v $version_num$bf_type -w $checkout_addr
defects4j checkout -p $project_id -v $version_num$bf_type -w $checkout_addr

# 编译checkout
#echo defects4j compile -w $checkout_addr
defects4j compile -w $checkout_addr

# 编译并执行mannual测试用例
#echo defects4j test_diy -w $checkout_addr -o $ant_log_output -a $ant_build_file_addr
defects4j test_diy -w $checkout_addr -o $ant_log_output -a $ant_build_file_addr
