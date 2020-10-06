#!/usr/bin/env bash

# 第一个参数$1表示 DEFECTS4J_PRE_SOURCE_FILE_ADDR
# 第二个参数$2表示 DEFECTS4J_PRE_INCLUDE_FILE_ADDR
# 第二个参数$3表示 输出文件位置
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

<<com
# run_randoop.plçš„å‚æ•°å®šä¹‰
run_randoop.pl
    Usage:
          run_randoop.pl -p project_id -v version_id -n test_id -o out_dir -b budget [-t tmp_dir_gen] [-D]
    
    Options:
        -p "project_id"
            Generate tests for this project id. See Project module for available
            project IDs.
    
        -v "version_id"
            Generate tests for this version id. Format: "\d+[bf]".
    
        -n "test_id"
            The id of the generated test suite (i.e., which run of the same
            configuration).
    
        -o out_dir
            The root output directory for the generated test suite. The test
            suite and logs are written to: out_dir/project_id/version_id.
    
        -b "budget"
            The time in seconds allowed for test generation.
    
        -t tmp_dir_gen
            The temporary root directory to be used to check out the program
            version (optional). The default is /tmp.
    
        -D  Debug: Enable verbose logging and do not delete the temporary
            check-out directory (optional).
com


# run_randoop.pl -p Lang -v 2f -n 1 -o /tmp/test_d4j/randoop -b 10
suite_src=randoop
suite_num=1         #

project_id=Lang     #
version_num=2       #
bf_type=b           #

version_id=$version_num$bf_type

test_id=1           #
out_dir=$TMP_DIR
budget=20
tmp_dir_gen=$TMP_DIR/tmp_gen
tmp_dir_fix=$TMP_DIR/tmp_fix
suite_dir=$out_dir/$project_id/$suite_src/$suite_num

# Run Randoop and fix test suite
# 生成测试用例（压缩包）
run_randoop.pl -p $project_id -v $version_id -n $test_id -o $out_dir -b $budget -t $tmp_dir_gen
# 对测试用例做fix 删除不可用的测试用例（压缩包即可）
fix_test_suite.pl -p $project_id -d $suite_dir -t $tmp_dir_fix || die "fix test suite"


