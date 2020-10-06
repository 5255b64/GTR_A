# TODO 重构

"""
对于给定的程序版本
生成测试用例
"""
import os
import sys

from src.utils import sub_call_hook, file_helper
from src.utils.defects4j import check_proj_args
from src.CONFIG import DEFECTS4J_PRE_SOURCE_FILE_ADDR, DEFECTS4J_PRE_INCLUDE_FILE_ADDR, \
    BASH_DEFECT4J_GEN_TESTCASE


def run(output_addr: str, project_id: str, version_num: int, bf_type: str, suite_num: str = "1", test_id: int = 1,
        budget: int = 20, suite_src: str = "randoop"):
    """

    :param output_addr:     测试用例输出地址
    :param project_id:      项目名（如Lang）
                            Generate tests for this project id. See Project module for available project IDs.
    :param version_num:     版本号 数字
    :param bf_type:         f或者b（代表fixed和buggy）
    :param suite_num:       测试集编号 代表同一个项目中不同测试集的序号 只影响测试集的存储路径
    :param test_id:         The id of the generated test suite (i.e., which run of the same configuration).
    :param budget:          生成测试用例的时间限制（秒）
                            The time in seconds allowed for test generation.
    :param suite_src:       使用的测试用例生成工具（randoop或者evosuite）
    :return:testcase_addr   生成的测试用例地址
    """
    is_passed = True
    if not check_proj_args(project_id, version_num, bf_type):
        is_passed = False
        sys.stderr.write("if_bash_Defects4jGenTestcase.py:项目参数验证不通过")

    if suite_src not in ["randoop", "evosuite"]:
        is_passed = False
        sys.stderr.write("if_bash_Defects4jGenTestcase.py: suite_src只能是randoop或者evosuite")

    if is_passed:
        tmp_folder = output_addr + os.sep + "/tmp_if_bash_Defects4jGenTestcase"
        cmd = ["bash",
               # "-x",
               BASH_DEFECT4J_GEN_TESTCASE,
               DEFECTS4J_PRE_SOURCE_FILE_ADDR,  # $1
               DEFECTS4J_PRE_INCLUDE_FILE_ADDR,  # $2
               output_addr,  # $3
               project_id,  # $4
               str(version_num),  # $5
               bf_type,  # $6
               suite_num,  # $7
               str(test_id),  # $8
               str(budget),  # $9
               tmp_folder,  # $10
               suite_src,  # $11
               ]
        # print(" ".join(cmd))
        sub_call_hook.serial(cmd)
        testcase_addr = output_addr + os.sep + project_id + os.sep + suite_src + os.sep + suite_num

        # 删除临时文件
        # cmd = ["rm", "-rf", tmp_folder]
        # sub_call_hook.serial(cmd)
        file_helper.rm(tmp_folder)

        return testcase_addr
    else:
        return -1


if __name__ == "__main__":
    result = run(output_addr="/tmp/xxx", project_id="Lang", version_num=4, bf_type="f")
    print(result)
