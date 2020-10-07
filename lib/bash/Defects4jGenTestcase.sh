#!/usr/bin/env bash
# 生成randoop和evosuite的测试用例

# 第一个参数$1表示 DEFECTS4J_PRE_SOURCE_FILE_ADDR
# 第二个参数$2表示 DEFECTS4J_PRE_INCLUDE_FILE_ADDR
# 第二个参数$3表示 测试用例位置
# 第二个参数$4表示 
# 第二个参数$5表示 
# 第二个参数$6表示 

# 加载defects4j环境变量
# export DEFECT4J_PATH=/home/gx/Code/TestMinimization/defects4j-master
source $1

# 加载.include文件
# source diy.include
source $2
init

export "TMP_DIR=$3"
mkdir $3

# run_randoop.pl -p Lang -v 2f -n 1 -o /tmp/test_d4j/randoop -b 10


project_id=$4     # $4
version_num=$5       # $5
bf_type=$6           # $6

version_id=$version_num$bf_type

suite_num=$7         # $7
test_id=$8           # $8
out_dir=$TMP_DIR
budget=$9           # $9
checkout_folder=${10}  # $10
suite_src=${11}   # $11
classes_file=${12} # $12
suite_dir=$out_dir/$project_id/$suite_src/$suite_num

# Run Randoop and fix test suite
# 生成测试用例（压缩包）
# echo gen_tests.pl -g suite_src -p $project_id -v $version_id -n $test_id -o $out_dir -b $budget -t $tmp_dir/tmp_gen
gen_tests.pl -g $suite_src -p $project_id -v $version_id -n $test_id -o $out_dir -b $budget -t $checkout_folder
# 对测试用例做fix 删除不可用的测试用例（压缩包即可）
fix_test_suite.pl -p $project_id -d $suite_dir -t $checkout_folder|| die "fix test suite"



