# TODO 重构
"""
针对一个version
gen testsuite
"""
import glob
import os

from interface.bash import Defects4jCheckout, Defects4jGenTestcase
from src.CONFIG import TMP_FOLDER, TMP_TEST_FOLDER
from src.utils import sub_call_hook, file_helper


#  1）生成测试用例
#       out:   测试用例（原始）
def run(output_addr: str, checkout_folder:str, project_id: str, version_num: int, bf_type: str,
        suite_num: str = "1", test_id: int = 1, budget: int = 20, suite_src: str = "randoop"):
    """

    :param output_addr:                         输出结果 原测试用例集的位置
    :param checkout_folder:                     checkout地址 若不存在checkout 则会自动生成
    :param project_id:                          项目名（如Lang）
                                                Generate tests for this project id. See Project module for available project IDs.
    :param version_num:                         版本号 数字
    :param bf_type:                             f或者b（代表fixed和buggy）
    :param suite_num:                           测试集编号 代表同一个项目中不同测试集的序号 只影响测试集的存储路径
    :param test_id:                             The id of the generated test suite (i.e., which run of the same configuration).
    :param budget:                              生成测试用例的时间限制（秒）
                                                The time in seconds allowed for test generation.
    :param suite_src:                           使用的测试用例生成工具（randoop或者evosuite）
    :return:
    """
    # 确保路径存在
    file_helper.check_path_exists(output_addr)

    # 返回值
    return_ouput_testcase_addr = None

    if suite_src == "mannual":
        # TODO 获取手工测试用例
        return_ouput_testcase_addr = Defects4jCheckout.run(
            project_id=project_id,
            version_num=version_num,
            bf_type=bf_type,
            suite_num=suite_num,
            suite_src=suite_src,
            output_addr=output_addr
        )
    else:
        # 第三方工具生成测试用例
        # 默认会进行checkout
        return_ouput_testcase_addr = Defects4jGenTestcase.run(
            checkout_folder=checkout_folder,
            project_id=project_id,
            version_num=version_num,
            bf_type=bf_type,
            suite_num=suite_num,
            suite_src=suite_src,
            output_addr=output_addr,
            test_id=test_id,
            budget=budget
        )

    return return_ouput_testcase_addr


if __name__ == "__main__":
    suite_src = "randoop"
    project_id = "Lang"
    version_num = 1
    bf_type = "b"
    output_addr = TMP_TEST_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type

    # 提前checkout
    # Defects4jCheckout.run(project_id=project_id, version_num=version_num, bf_type=bf_type,
    #     output_addr=output_addr)

    run(
        checkout_folder=output_addr,
        output_addr=output_addr,
        project_id=project_id,
        version_num=version_num,
        bf_type=bf_type,
        suite_src=suite_src
    )
