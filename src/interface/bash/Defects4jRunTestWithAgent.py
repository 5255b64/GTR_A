"""
在使用agent的情况下
运行指定的testsuite（bz2压缩包形式）

注意：
1）需要事先将测试用例打包
2）需要事先准备好build文件
"""
import os

from src.utils import sub_call_hook
from src.CONFIG import DEFECTS4J_ADD_PATH_FILE, DEFECTS4J_PRE_INCLUDE_FILE_ADDR, \
    BASH_DEFECT4J_RUN_TEST_WITH_AGENT
from utils import file_helper


def run(output_addr: str, checkout_addr: str, testsuite_addr: str, build_file: str):
    """
    defects4j test_diy 将会产生 ant 日志
    从ant日志中 分析出 junit日志 作为输出
    :param output_addr:         junit日志输出地址
                                    Generate tests for this project id. See Project module for available project IDs.
    :param checkout_addr:       项目checkout的路径
    :param testsuite_addr:      testsuite路径 是一个.bz2压缩包
    :param build_file:          build file 路径
    :return:testcase_addr:      生成的测试用例地址
    """
    # 临时文件 ant日志
    tmp_log = output_addr + "_ant"

    file_helper.check_file_exists(output_addr)

    working_directory = checkout_addr + os.sep + "checkout"

    cmd = ["bash",
           # "-x",
           BASH_DEFECT4J_RUN_TEST_WITH_AGENT,
           DEFECTS4J_ADD_PATH_FILE,  # $1
           DEFECTS4J_PRE_INCLUDE_FILE_ADDR,  # $2
           working_directory,  # $3
           tmp_log,  # $4
           testsuite_addr,  # $5
           build_file,  # $6
           ]
    # print(" ".join(cmd))
    sub_call_hook.serial(cmd)

    # 分析ant日志 获取junit日志

    parse(intput_ant_log=tmp_log, output_junit_log=output_addr)

    # 删除临时文件
    # file_helper.rm(tmp_log)


def parse(intput_ant_log, output_junit_log):
    """
    从ant日志中 抽取junit日志
    :param intput_ant_log:
    :param output_junit_log:
    :return:
    """
    with open(intput_ant_log, 'r') as f_in:
        with open(output_junit_log, 'w') as f_out:
            line = f_in.readline()
            # 只考虑run.gen.tests.withjavaagent之后的阶段
            while not line.startswith("run.gen.tests.withjavaagent"):
                line = f_in.readline()

            while line:
                if line.replace(" ", "").startswith("[junit]"):
                    args = line.split(" ")
                    out_args = []
                    for temp in args:
                        if temp != "" and temp != "[junit]":
                            out_args.append(temp)
                    f_out.write(" ".join(out_args))
                line = f_in.readline()


def parser_test():
    parse("/tmp/tmp/log", "/tmp/tmp/log2")


def run_test():
    output_addr = "/tmp/tmp/log"
    checkout_addr = "/home/gx/Documents/TestMinimization/GTR_A/tmp/test/Lang/1b/"
    testsuite_addr = "/home/gx/Documents/TestMinimization/GTR_A/tmp/test/Lang/1b/randoop/1b.tar.bz2"
    build_file = "/home/gx/Documents/TestMinimization/GTR_A/lib/defects4j_cfg/defects4j.build.template.xml"
    run(
        output_addr=output_addr,
        checkout_addr=checkout_addr,
        testsuite_addr=testsuite_addr,
        build_file=build_file
    )


if __name__ == "__main__":
    run_test()
    # parser_test()