#!/usr/bin/env bash

# 第一个参数$1表示 DEFECTS4J_PRE_SOURCE_FILE_ADDR
# 第二个参数$2表示 DEFECTS4J_PRE_INCLUDE_FILE_ADDR

# 加载defects4j环境变量
source $1

# 加载.include文件
# source diy.include
source $2
init

export "TMP_DIR=$3"
mkdir $3



project_id=$4     # $4
version_num=$5       # $5
bf_type=$6           # $6

version_id=$version_num$bf_type

suite_dir=$7           # $7

# Checkout
# echo defects4j checkout -p $project_id -v $version_id -w $suite_dir
defects4j checkout -p $project_id -v $version_id -w $suite_dir

# Compile
# echo defects4j compile -w $suite_dir
defects4j compile -w $suite_dir


