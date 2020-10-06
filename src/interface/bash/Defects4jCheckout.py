# TODO 重构

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


def run(project_id: str, version_num: int, bf_type: str, suite_num: str = "1",
        output_addr: str = TMP_FOLDER,
        suite_src: str = "randoop"):
    """

    :param project_id:      项目名（如Lang）
                            Generate tests for this project id. See Project module for available project IDs.
    :param version_num:     版本号 数字
    :param bf_type:         f或者b（代表fixed和buggy）
    :param suite_num:       测试集编号 代表同一个项目中不同测试集的序号 只影响测试集的存储路径
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
        # bash脚本生成的临时文件目录（需要删除）
        tmp_root_folder = output_addr + "/tmp_if_bash_Defects4jCheckout"
        cmd = ["bash",
               # "-x",
               BASH_DEFECT4J_CHECKOUT,
               DEFECTS4J_ADD_PATH_FILE,  # $1
               DEFECTS4J_PRE_INCLUDE_FILE_ADDR,  # $2
               tmp_root_folder,  # $3
               project_id,  # $4
               str(version_num),  # $5
               bf_type,  # 6
               checkout_addr,  # $7
               ]
        # print(" ".join(cmd))
        sub_call_hook.serial(cmd)

        # 删除临时文件
        file_helper.rm(tmp_root_folder)

        # TODO 提取测试用例
        # 不同的项目 其测试用例的存储路径不同
        testcase_source_addr = "-1"  # 保存所有测试用例的文件
        for source_addr in PROJ_TEST_SOURCE_ADDR_LIST:
            testcase_source_addr = checkout_addr + os.sep + source_addr
            if os.path.exists(testcase_source_addr):
                break
        if testcase_source_addr == "-1":
            raise Exception("引用了记录之外的项目:\t" + project_id + "-" + str(version_num))

        # TODO 压缩测试用例
        testcase_addr = checkout_addr + os.sep + project_id + "-" + str(
            version_num) + bf_type + "-" + suite_src + "." + suite_num + ".tar.bz2"

        # bz2_helper.compress(input_addr=testcase_source_addr, output_bz2_file_name=testcase_addr)
        if os.path.exists(testcase_addr):
            file_helper.rm(testcase_addr)

        return checkout_addr


if __name__ == "__main__":
    suite_src = "mannual"
    project_id = "Chart"
    version_num = 1
    bf_type = "b"
    output_addr = TMP_TEST_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type
    result = run(project_id=project_id, version_num=version_num, bf_type=bf_type,
                 output_addr=output_addr, suite_src=suite_src)
    print(result)
