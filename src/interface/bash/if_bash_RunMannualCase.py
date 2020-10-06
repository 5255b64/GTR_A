# TODO 重构

"""
对于给定的程序版本
生成测试用例
"""
import sys

from src.CONFIG import DEFECTS4J_PRE_SOURCE_FILE_ADDR, BASH_RUN_MANNUAL_CASE_WITH_JAVAAGENT, \
    DEFECTS4J_PROJ_BUILD_FILE_ADDR, TMP_ROOT_FOLDER, BASH_RUN_MANNUAL_CASE
from src.utils import sub_call_hook, file_helper
from src.utils.defects4j import check_proj_args


def run(project_id: str, version_num: int, bf_type: str, output_checkout_path: str, falling_test_addr:str):
    """

    :param falling_test_addr:           保存执行失败的
    :param output_checkout_path:
    :param project_id:      项目名（如Lang）
                            Generate tests for this project id. See Project module for available project IDs.
    :param version_num:     版本号 数字
    :param bf_type:         f或者b（代表fixed和buggy）
    :return:
    """
    is_passed = True
    if not check_proj_args(project_id, version_num, bf_type):
        is_passed = False
        sys.stderr.write("if_bash_Defects4jGenTestcase.py:项目参数验证不通过")

    if is_passed:
        # 清空checkout路径
        # cmd = ["rm", "-rf", checkout_addr]
        # sub_call_hook.serial(" ".join(cmd))
        file_helper.rm(output_checkout_path)

        # 创建checkout路径
        file_helper.check_path_exists(output_checkout_path)

        cmd = ["bash",
               # "-x",
               BASH_RUN_MANNUAL_CASE,
               DEFECTS4J_PRE_SOURCE_FILE_ADDR,  # $1
               output_checkout_path,  # $2
               project_id,  # $3
               str(version_num),  # $4
               bf_type,  # 5
               falling_test_addr, # 6
               ]
        # print(" ".join(cmd))
        sub_call_hook.serial(cmd)


if __name__ == "__main__":
    pass
