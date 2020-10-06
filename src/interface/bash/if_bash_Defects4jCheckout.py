# TODO 重构

"""
对于给定的程序版本
生成测试用例
"""
import os
import sys

from src.utils.defects4j import check_proj_args
from src.CONFIG import DEFECTS4J_PRE_SOURCE_FILE_ADDR, DEFECTS4J_PRE_INCLUDE_FILE_ADDR, \
    TMP_ROOT_FOLDER, BASH_DEFECT4J_CHECKOUT, PROJ_TEST_SOURCE_ADDR_LIST
from src.utils import sub_call_hook, file_helper, bz2_helper


def run(project_id: str, version_num: int, bf_type: str, suite_num: str = "1",
        output_addr: str = TMP_ROOT_FOLDER,
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
    is_passed = True
    if not check_proj_args(project_id, version_num, bf_type):
        is_passed = False
        sys.stderr.write("if_bash_Defects4jGenTestcase.py:项目参数验证不通过")

    if is_passed:
        # suite_dir = output_addr + os.sep + project_id + os.sep + suite_src + os.sep + str(version_num)
        suite_dir = output_addr + "/checkout"
        file_helper.check_path_exists(suite_dir)
        tmp_root_folder = output_addr + "/tmp_if_bash_Defects4jCheckout"
        cmd = ["bash",
               # "-x",
               BASH_DEFECT4J_CHECKOUT,
               DEFECTS4J_PRE_SOURCE_FILE_ADDR,  # $1
               DEFECTS4J_PRE_INCLUDE_FILE_ADDR,  # $2
               tmp_root_folder,  # $3
               project_id,  # $4
               str(version_num),  # $5
               bf_type,  # 6
               suite_dir,  # $7
               ]
        # print(" ".join(cmd))
        sub_call_hook.serial(cmd)

        # 删除临时文件
        # cmd = ["rm", "-rf", tmp_root_folder]
        # sub_call_hook.serial(" ".join(cmd))

        # 不同的项目 其测试用例的存储路径不同
        testcase_source_addr = "-1"  # 保存所有测试用例的文件
        for source_addr in PROJ_TEST_SOURCE_ADDR_LIST:
            testcase_source_addr = suite_dir + os.sep + source_addr
            if os.path.exists(testcase_source_addr):
                break
        if testcase_source_addr == "-1":
            raise Exception("引用了记录之外的项目:\t"+project_id+"-"+str(version_num))

        testcase_addr = suite_dir + os.sep + project_id + "-" + str(
            version_num) + bf_type + "-" + suite_src + "." + suite_num + ".tar.bz2"

        # bz2_helper.compress(input_addr=testcase_source_addr, output_bz2_file_name=testcase_addr)
        if os.path.exists(testcase_addr):
            file_helper.rm(testcase_addr)

        return suite_dir
    else:
        return -1


if __name__ == "__main__":
    result = run(project_id="Chart", version_num=1, bf_type="f",
                 output_addr="/tmp/xxx", suite_src="mannual")
    print(result)
