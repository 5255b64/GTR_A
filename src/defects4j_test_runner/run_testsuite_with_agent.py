"""
插桩 执行测试用例
得到junit日志

流程：
1）提前进行checkout
2）提前准备.bz2测试用例
3）提前生成build文件
4）调用interface进行测试用例执行 获得日志
"""
import os

from CONFIG import TMP_TEST_FOLDER, JAVAAGENT_ARGS_PREFIX, DEFECTS4J_PROJ_INFO_ADDR, DEFECTS4J_ANT_BUILD_TEMPLATE_ADDR
from defects4j_test_generator import gen_testsuite_version
from interface.bash import Defects4jRunTestWithAgent
from interface.java import if_java_AntBuildFileEditor


def run(checkout_addr: str, testsuite_addr: str, output_junit_log_addr: str, tmp_build_file_addr: str, project_id: str,
        version_num: int, bf_type: str, suite_num: str = "1", test_id: int = 1, budget: int = 20,
        suite_src: str = "randoop"):
    """

    :param checkout_addr:                       输出 存放checkout的地址
    :param testsuite_addr:                      输出 存放testsuite的地址
    :param output_junit_log_addr:               输出 存放junit日志的地址
    :param tmp_build_file_addr:                 临时文件 build文件的位置
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
    # 1）进行checkout（不需要 步骤2会自动生成）

    # 2）生成.bz2测试用例
    # 目标测试用例文件 若已存在则不生成
    testsuite = testsuite_addr + os.sep + suite_src + os.sep + str(version_num) + bf_type + ".tar.bz2"
    # if not os.path.exists(testsuite):
    gen_testsuite_version.run(
        checkout_folder=checkout_addr,
        output_addr=testsuite_addr,
        project_id=project_id,
        version_num=version_num,
        bf_type=bf_type,
        suite_src=suite_src
    )
    # # 3）生成build文件
    # if not os.path.exists(tmp_build_file_addr):
    output_err_path = tmp_build_file_addr + ".output.err"
    output_alltest_path = tmp_build_file_addr + ".alltest.err"
    set_build_file(
        project_id=project_id,
        version_num=version_num,
        output_err_path=output_err_path,
        output_alltest_path=output_alltest_path,
        output_build_file_addr=tmp_build_file_addr,
    )
    # 4）执行测试用例 获取日志
    # if not os.path.exists(output_junit_log_addr):
    Defects4jRunTestWithAgent.run(
        output_addr=output_junit_log_addr,
        checkout_addr=checkout_addr,
        testsuite_addr=testsuite,
        build_file=tmp_build_file_addr
    )


def set_build_file(project_id: str, version_num: int, output_err_path: str, output_alltest_path: str,
                   output_build_file_addr: str):
    """

    :param project_id:
    :param version_num:
    :param output_err_path:                未知
    :param output_alltest_path:            未知
    :param output_build_file_addr:         输出 生成的build文件模板
    :return:
    """
    # 找到项目文件夹
    file_addr = DEFECTS4J_PROJ_INFO_ADDR + os.sep + project_id + os.sep + "loaded_classes" + os.sep + str(
        version_num) + ".src"
    agent_args = JAVAAGENT_ARGS_PREFIX
    with open(file_addr, 'r') as f:
        lines = f.readlines()
        if len(lines) > 0:
            agent_args += "=includes="
            for line in lines:
                agent_args += line.replace('\n', "") + ":"
                # print(line)
            # 删除最后一个:号
            agent_args = agent_args[0:len(agent_args) - 2]
    # print(agent_args)
    if_java_AntBuildFileEditor.run(
        inputFileAddr=DEFECTS4J_ANT_BUILD_TEMPLATE_ADDR,
        # outputFileAddr=DEFECTS4J_PROJ_BUILD_FILE_ADDR,
        outputFileAddr=output_build_file_addr,
        javaagentArgs=agent_args,
        outputErrPath=output_err_path,
        outputAlltestPath=output_alltest_path
    )


if __name__ == "__main__":
    suite_src = "randoop"
    project_id = "Lang"
    version_num = 1
    bf_type = "b"
    output_junit_log_addr = TMP_TEST_FOLDER + os.sep + project_id + os.sep + str(
        version_num) + bf_type + os.sep + suite_src + os.sep + "junit.log"
    build_file_addr = TMP_TEST_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type + os.sep + "build.xml"
    output_checkout_addr = TMP_TEST_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type
    output_testsuite_addr = TMP_TEST_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type

    run(
        checkout_addr=output_checkout_addr,
        testsuite_addr=output_testsuite_addr,
        output_junit_log_addr=output_junit_log_addr,
        tmp_build_file_addr=build_file_addr,
        project_id=project_id,
        version_num=version_num,
        bf_type=bf_type,
        suite_src=suite_src
    )
