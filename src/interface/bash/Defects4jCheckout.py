"""
对于给定的程序版本
生成测试用例
"""
import os
import sys

from src.utils.defects4j import check_proj_args
from src.CONFIG import DEFECTS4J_ADD_PATH_FILE, DEFECTS4J_PRE_INCLUDE_FILE_ADDR, \
    TMP_FOLDER, BASH_DEFECT4J_CHECKOUT, PROJ_TEST_SOURCE_ADDR_LIST, TMP_TEST_FOLDER
from src.utils import sub_call_hook, file_helper, bz2_helper


def run(project_id: str, version_num: int, bf_type: str, output_addr: str = TMP_FOLDER):
    """

    :param project_id:      项目名（如Lang）
                            Generate tests for this project id. See Project module for available project IDs.
    :param version_num:     版本号 数字
    :param bf_type:         f或者b（代表fixed和buggy）
    :param output_addr:     生成checkout的保存路径
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
               BASH_DEFECT4J_CHECKOUT,
               DEFECTS4J_ADD_PATH_FILE,  # $1
               DEFECTS4J_PRE_INCLUDE_FILE_ADDR,  # $2
               project_id,  # $3
               str(version_num),  # $4
               bf_type,  # 5
               checkout_addr,  # $6
               ]
        # print(" ".join(cmd))
        sub_call_hook.serial(cmd)

        return checkout_addr


if __name__ == "__main__":
    project_id = "Lang"
    version_num = 1
    bf_type = "b"
    output_addr = TMP_TEST_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type
    result = run(project_id=project_id, version_num=version_num, bf_type=bf_type,
                 output_addr=output_addr)
    print(result)
