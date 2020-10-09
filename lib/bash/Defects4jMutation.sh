#!/usr/bin/env bash

# 第一个参数$1表示 DEFECTS4J_PRE_SOURCE_FILE_ADDR
# 第二个参数$2表示 DEFECTS4J_PRE_INCLUDE_FILE_ADDR

# 加载defects4j环境变量
source $1

# 加载.include文件
# source diy.include
source $2
init

#export "TMP_DIR=$3"
#mkdir $3



project_id=$3     # $3
version_num=$4       # $4
bf_type=$5           # $5
checkout_addr=$6           # $6
suite_addr=$7         # $7
suite_src=$8          # $8

version_id=$version_num$bf_type

# Checkout
#echo defects4j checkout -p $project_id -v $version_id -w $checkout_addr
defects4j checkout -p $project_id -v $version_id -w $checkout_addr

# Mutation
if [ $suite_src == "mannual" ]; then
  defects4j mutation -w $checkout_addr
else
  defects4j mutation -w $checkout_addr -s $suite_addr
fi
