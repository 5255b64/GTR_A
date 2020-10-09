"""
在指定checkout上 获取变异测试结果
注意：尽量在fixed版本上进行变异操作
"""
import os

from CONFIG import TMP_TEST_FOLDER
from interface.bash import Defects4jMutation
from utils import file_helper


def run(input_suite_addr: str, project_id: str, version_num: int, bf_type: str, checkout_addr: str, output_addr: str,
        suite_src: str):
    """
    :param input_suite_addr:        输入测试用例的地址(对于mannual测试用例来说是不需要的）
    :param project_id:              项目名（如Lang）
                                    Generate tests for this project id. See Project module for available project IDs.
    :param version_num:             版本号 数字
    :param bf_type:                 f或者b（代表fixed和buggy）
    :param checkout_addr:           生成checkout的保存路径
    :param output_addr:             生成Mutation结果的路径
    :param suite_src:       使用的测试用例生成工具（randoop或者evosuite）
    :return:
    """
    checkout_tmp_addr = checkout_addr
    output_tmp_addr = output_addr

    # 执行bash脚本
    Defects4jMutation.run(
        input_suite_addr=input_suite_addr,
        project_id=project_id,
        version_num=version_num,
        bf_type=bf_type,
        output_addr=checkout_tmp_addr,
        suite_src=suite_src,
    )
    if suite_src == "mannual":
        bf_type = "b"

    # 将输出结果copy至output路径
    file_helper.cp(checkout_tmp_addr + os.sep + "checkout" + os.sep + "mutants.log", output_tmp_addr
                   + os.sep + suite_src + os.sep + "mutants.log", )
    file_helper.cp(checkout_tmp_addr + os.sep + "checkout" + os.sep + "testMap.csv", output_tmp_addr
                   + os.sep + suite_src + os.sep + "testMap.csv", )
    file_helper.cp(checkout_tmp_addr + os.sep + "checkout" + os.sep + "kill.csv", output_tmp_addr
                   + os.sep + suite_src + os.sep + "kill.csv", )
    file_helper.cp(checkout_tmp_addr + os.sep + "checkout" + os.sep + "summary.csv", output_tmp_addr
                   + os.sep + suite_src + os.sep + "summary.csv", )


if __name__ == "__main__":
    project_id = "Chart"
    version_num = 2
    bf_type = "f"
    suite_src = "randoop"
    checkout_addr = TMP_TEST_FOLDER
    output_addr = TMP_TEST_FOLDER + os.sep + "mutation"
    if suite_src == "mannual":
        input_suite_addr = "xxx"  # (对于mannual测试用例来说是不需要的）
    else:
        input_suite_addr = checkout_addr + os.sep + project_id + os.sep + str(
            version_num) + bf_type + os.sep + suite_src + ".tar.bz2"
    run(
        input_suite_addr=input_suite_addr,
        project_id=project_id,
        version_num=version_num,
        bf_type=bf_type,
        checkout_addr=checkout_addr,
        output_addr=output_addr,
        suite_src=suite_src,
    )
