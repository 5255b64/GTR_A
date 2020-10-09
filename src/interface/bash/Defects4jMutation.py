"""
对于给定的程序版本
生成测试用例
"""
import os
import sys

from src.utils.defects4j import check_proj_args
from src.CONFIG import DEFECTS4J_ADD_PATH_FILE, DEFECTS4J_PRE_INCLUDE_FILE_ADDR, \
    TMP_FOLDER, TMP_TEST_FOLDER, BASH_DEFECT4J_MUTATION
from src.utils import sub_call_hook, file_helper


def run(input_suite_addr: str, project_id: str, version_num: int, bf_type: str, output_addr: str,
        suite_src: str = "not mannual"):
    """

    :param input_suite_addr:      输入测试用例的地址
    :param project_id:      项目名（如Lang）
                            Generate tests for this project id. See Project module for available project IDs.
    :param version_num:     版本号 数字
    :param bf_type:         f或者b（代表fixed和buggy）
    :param output_addr:     生成checkout的保存路径
    :param suite_src:       使用的测试用例生成工具（randoop或者evosuite）
    :return:testcase_addr   生成的测试用例地址
    """
    if not check_proj_args(project_id, version_num, bf_type):
        sys.stderr.write("interface/bash/Defects4jGenTestcase.py:项目参数验证不通过")
        return None
    else:
        # 注意 必须要在一个新的文件夹（checkout）中进行checkout操作 否则不成功
        checkout_addr = output_addr + os.sep + "checkout"
        file_helper.check_path_exists(checkout_addr)

        cmd = ["bash",
               # "-x",
               BASH_DEFECT4J_MUTATION,
               DEFECTS4J_ADD_PATH_FILE,  # $1
               DEFECTS4J_PRE_INCLUDE_FILE_ADDR,  # $2
               project_id,  # $3
               str(version_num),  # $4
               bf_type,  # 5
               checkout_addr,  # $6
               input_suite_addr,  # $7
               suite_src,  # $8
               ]
        # print(" ".join(cmd))
        sub_call_hook.serial(cmd)


if __name__ == "__main__":
    project_id = "Lang"
    version_num = 1
    bf_type = "f"
    suite_src = "mannual"
    # suite_src = "randoop"
    input_suite_addr = TMP_TEST_FOLDER + os.sep + project_id + os.sep + str(
        version_num) + bf_type + os.sep + "1b.tar.bz2"
    # input_suite_addr = "xxx"
    output_addr = TMP_TEST_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type
    run(
        input_suite_addr=input_suite_addr,
        project_id=project_id,
        version_num=version_num,
        bf_type=bf_type,
        output_addr=output_addr,
        suite_src=suite_src
    )
