"""
针对一个version
gen testsuite
"""
import os

from src.interface.bash import Defects4jCheckout, Defects4jGenTestcase
from src.CONFIG import TMP_TEST_FOLDER, PROJ_TEST_SOURCE_ADDR_LIST, DEFECTS4J_PROJ_INFO_ADDR
from src.utils import file_helper, test_suite_fixer, bz2_helper


def run(output_addr: str, checkout_folder: str, project_id: str, version_num: int, bf_type: str,
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
    checkout_tmp_folder = checkout_folder

    output_tmp_addr = output_addr

    # 确保路径存在
    file_helper.check_path_exists(output_addr)

    # 返回值
    tmp_output_testcase_addr = None

    if suite_src == "manual":
        # 获取手工测试用例
        # 先checkout 然后根据test可能的路径进行查找
        Defects4jCheckout.run(
            project_id=project_id,
            version_num=version_num,
            bf_type=bf_type,
            output_addr=checkout_tmp_folder
        )
        # 查找manual测试用例
        # 不同的项目 其测试用例的存储路径不同
        wordking_directory = checkout_tmp_folder + os.sep + "checkout"

        testcase_source_addr = None
        for source_addr in PROJ_TEST_SOURCE_ADDR_LIST:
            testcase_source_addr = wordking_directory + os.sep + source_addr
            if os.path.exists(testcase_source_addr):
                break
        if testcase_source_addr is None:
            raise Exception("引用了记录之外的项目:\t" + project_id + "-" + str(version_num))

        tmp_output_testcase_addr = output_tmp_addr + os.sep + "manual"
        file_helper.cp(testcase_source_addr, tmp_output_testcase_addr)
    else:
        # 第三方工具生成测试用例
        # 默认会进行checkout
        tmp_output_testcase_addr = Defects4jGenTestcase.run(
            checkout_folder=checkout_tmp_folder,
            project_id=project_id,
            version_num=version_num,
            bf_type=bf_type,
            suite_num=suite_num,
            suite_src=suite_src,
            output_addr=output_tmp_addr,
            test_id=test_id,
            budget=budget
        )
    # 修改所有测试用例 并压缩
    if suite_src != "manual":
        for file in file_helper.getallfile(tmp_output_testcase_addr):
            if file.endswith(".java"):
                bkb_file = file + ".bkb"
                file_helper.cp(file, bkb_file)
                test_suite_fixer.fun(input_file_addr=bkb_file, output_file_addr=file)
    else:
        # manual情况做特殊处理
        tmp_tmp_ouput_testcase_addr = tmp_output_testcase_addr + "_tmp"
        file_helper.check_path_exists(tmp_tmp_ouput_testcase_addr)
        relevant_tests_file = DEFECTS4J_PROJ_INFO_ADDR + os.sep + project_id + os.sep + "relevant_tests" + os.sep + str(
            version_num)
        with open(relevant_tests_file, 'r') as f:
            line = f.readline()
            while line:
                test_case_file = tmp_output_testcase_addr + os.sep + line.replace(os.linesep, "").replace(".",
                                                                                                         os.sep) + ".java"
                tmp_test_case_file = tmp_tmp_ouput_testcase_addr + os.sep + line.replace(os.linesep, "").replace(".",
                                                                                                                 os.sep) + ".java"
                test_suite_fixer.fun(input_file_addr=test_case_file, output_file_addr=tmp_test_case_file)
                line = f.readline()
        tmp_output_testcase_addr = tmp_tmp_ouput_testcase_addr

    # 压缩
    fixed_testsuite_address = output_tmp_addr + os.sep + suite_src + ".tar.bz2"
    bz2_helper.compress(tmp_output_testcase_addr, fixed_testsuite_address)

    return fixed_testsuite_address


if __name__ == "__main__":
    suite_src = "manual"
    project_id = "Lang"
    version_num = 1
    bf_type = "f"
    output_addr = TMP_TEST_FOLDER
    checkout_folder = TMP_TEST_FOLDER

    run(
        checkout_folder=checkout_folder,
        output_addr=output_addr,
        project_id=project_id,
        version_num=version_num,
        bf_type=bf_type,
        suite_src=suite_src
    )
