#!/usr/bin/env bash

# 第一个参数$1表示 DEFECTS4J_PRE_SOURCE_FILE_ADDR
# 第二个参数$2表示 checkout的存储路径
# 第5个参数$3表示  project_id
# 第6个参数$4表示  version_num
# 第7个参数$5表示  bf_type

# 加载defects4j环境变量
# export DEFECT4J_PATH=/home/gx/Code/TestMinimization/defects4j-master
source $1

checkout_addr=$2
project_id=$3
version_num=$4
bf_type=$5
falling_test_addr=$6

# 生成checkout
echo defects4j checkout -p $project_id -v $version_num$bf_type -w $checkout_addr
defects4j checkout -p $project_id -v $version_num$bf_type -w $checkout_addr

# 编译
defects4j compile -w $checkout_addr

# 执行测试
# echo defects4j test -w $checkout_addr
defects4j test -w $checkout_addr > $falling_test_addr
