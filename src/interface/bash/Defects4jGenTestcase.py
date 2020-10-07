"""
对于给定的程序版本
生成randoop和evosuite的测试用例

针对所有 loaded class 生成测试用例
需要考虑以下参数：
  -c classes_file
         The file that lists all classes the test generator should target,
        one class per line (optional). By default, tests are generated only
         for classes modified by the bug fix.
defects4j默认只为 bug fix 的类生成测试用例
"""
import os
import sys

from src.utils import sub_call_hook, file_helper
from src.utils.defects4j import check_proj_args
from src.CONFIG import DEFECTS4J_ADD_PATH_FILE, DEFECTS4J_PRE_INCLUDE_FILE_ADDR, \
    BASH_DEFECT4J_GEN_TESTCASE, TMP_TEST_FOLDER, DEFECTS4J_PROJ_ADDR


def run(output_addr: str, checkout_folder: str, project_id: str, version_num: int, bf_type: str,
        suite_num: str = "1", test_id: int = 1,
        budget: int = 20, suite_src: str = "randoop"):
    """

    :param output_addr:     测试用例输出地址
    :param checkout_folder: checkout地址 若不存在checkout 则会自动生成
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
        sys.stderr.write("Defects4jGenTestcase.py:项目参数验证不通过")

    if suite_src not in ["randoop", "evosuite"]:
        is_passed = False
        sys.stderr.write("Defects4jGenTestcase.py: suite_src只能是randoop或者evosuite")

    if is_passed:
        testsuite_output_address = output_addr + os.sep + suite_src
        checkout_addr = checkout_folder + os.sep + "checkout"
        # 保存loaded class 的文件的路径
        loaded_classes_file = DEFECTS4J_PROJ_ADDR + os.sep + "framework" + os.sep + "projects" + os.sep + project_id + "loaded_classes" + os.sep + str(
            version_num) + ".src"
        cmd = ["bash",
               # "-x",
               BASH_DEFECT4J_GEN_TESTCASE,
               DEFECTS4J_ADD_PATH_FILE,  # $1
               DEFECTS4J_PRE_INCLUDE_FILE_ADDR,  # $2
               testsuite_output_address,  # $3
               project_id,  # $4
               str(version_num),  # $5
               bf_type,  # $6
               suite_num,  # $7
               str(test_id),  # $8
               str(budget),  # $9
               checkout_addr,  # $10
               suite_src,  # $11
               loaded_classes_file,  # $12
               ]
        # print(" ".join(cmd))
        sub_call_hook.serial(cmd)
        # testcase_addr = output_addr + os.sep + project_id + os.sep + suite_src + os.sep + suite_num

        # 删除临时文件
        # file_helper.rm(tmp_folder)

        # 将生成的测试用例压缩包 拷贝至浅层目录
        suite_src_file = testsuite_output_address + os.sep + project_id + os.sep + suite_src + os.sep + suite_num + os.sep + project_id + "-" + str(
            version_num) + bf_type + "-" + suite_src + "." + suite_num + ".tar.bz2"
        suite_dest_file = testsuite_output_address + os.sep + str(version_num) + bf_type + ".tar.bz2"
        file_helper.mv(src=suite_src_file, dest=suite_dest_file)

        return testsuite_output_address
    else:
        return None


if __name__ == "__main__":
    suite_src = "randoop"
    project_id = "Lang"
    version_num = 1
    bf_type = "b"
    output_addr = TMP_TEST_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type
    checkout_addr = output_addr
    result = run(
        output_addr=output_addr,
        checkout_folder= checkout_addr,
        project_id=project_id,
        version_num=version_num,
        bf_type=bf_type
    )
    print(result)
