# TODO 重构

"""
给定测试用例
在给定的程序版本上执行
得到 执行成功与否、覆盖率、变异分数 等数据
# 在linux bash上能跑过
# 用python调用bash会出错
# 原因是缺少了perl相关的环境变量
"""
import os
import sys

from src.utils import sub_call_hook
from src.utils.defects4j import check_proj_args
from src.CONFIG import DEFECTS4J_ADD_PATH_FILE, DEFECTS4J_PRE_INCLUDE_FILE_ADDR, TMP_FOLDER, \
    BASH_DEFECT4J_GET_TEST_RESULT


def run(project_id: str, version_num: int, bf_type: str, suite_num: str = "1", test_id: int = 1, budget: int = 20,
        tmp1: str = TMP_FOLDER, suite_src: str = "randoop"):
    """

    :param project_id:      项目名（如Lang）
                            Generate tests for this project id. See Project module for available project IDs.
    :param version_num:     版本号 数字
    :param bf_type:         f或者b（代表fixed和buggy）
    :param suite_num:       测试集编号 代表同一个项目中不同测试集的序号 只影响测试集的存储路径
    :param test_id:         The id of the generated test suite (i.e., which run of the same configuration).
    :param budget:          生成测试用例的时间限制（秒）
                            The time in seconds allowed for test generation.
    :param tmp1:        defects4j临时文件所在位置 可直接放到系统/tmp文件夹下
    :param suite_src:       使用的测试用例生成工具（randoop或者evosuite）
    :return:
    """
    is_passed = True
    if not check_proj_args(project_id, version_num, bf_type):
        is_passed = False
        sys.stderr.write("Defects4jGenTestcase.py:项目参数验证不通过")

    if suite_src not in ["randoop", "svosuite"]:
        is_passed = False
        sys.stderr.write("Defects4jGenTestcase.py: suite_src只能是randoop或者evosuite")

    if is_passed:
        tmp2 = TMP_FOLDER + os.sep + "tmp2"
        cmd = ["bash",
               # "-x",
               BASH_DEFECT4J_GET_TEST_RESULT,
               DEFECTS4J_ADD_PATH_FILE,  # $1
               DEFECTS4J_PRE_INCLUDE_FILE_ADDR,  # $2
               tmp2,  # $3
               project_id,  # $4
               str(version_num),  # $5
               bf_type,  # $6
               suite_num,  # $7
               str(test_id),  # $8
               str(budget),  # $9
               tmp1,  # $10
               suite_src,  # $11
               ]
        # print(" ".join(cmd))
        sub_call_hook.serial(cmd)

        # 删除临时文件
        # cmd = ["rm", "-rf", tmp_root_folder]
        # sub_call_hook.serial(" ".join(cmd))


if __name__ == "__main__":
    project_id = "Lang"
    version_num = 1
    bf_type = "b"
    tmp_addr = TMP_FOLDER + os.sep + "tmp1"

    run(
        project_id=project_id,
        version_num=version_num,
        bf_type=bf_type,
        tmp1=tmp_addr
    )
