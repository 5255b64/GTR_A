# TODO 重构

"""
对于给定的程序版本
执行某些测试用例
（通常要先插桩，获取桩数据）
"""
import os
import sys

from src.utils import sub_call_hook, file_helper
from src.utils.defects4j import check_proj_args
from src.CONFIG import PERL_RUN_TESTCASE_WITH_JAVA_AGENT, DEFECTS4J_PROJ_INFO_ADDR, \
    JAVAAGENT_ARGS_PREFIX, DEFECTS4J_ANT_BUILD_TEMPLATE_ADDR, TMP_ROOT_FOLDER, \
    PROJ_ROOT_PKG
from interface.java import if_java_AntBuildFileEditor


def run_with_buildfile(input_test_suite_addr: str, output_log_file: str, output_err_path: str, output_alltest_path: str,
                       project_id: str, ant_build_file_addr: str,
                       version_num: int, bf_type: str, suite_num: str = "1", test_id: int = 1,
                       suite_src: str = "randoop", tmp_folder: str = TMP_ROOT_FOLDER):
    # 生成build文件
    set_build_file(project_id, version_num, output_err_path, output_alltest_path, ant_build_file_addr)
    run_inner(input_test_suite_addr=input_test_suite_addr, output_log_file=output_log_file, project_id=project_id,
              version_num=version_num, bf_type=bf_type, suite_num=suite_num, test_id=test_id,
              suite_src=suite_src, tmp_folder=tmp_folder, ant_build_file_addr=ant_build_file_addr)


def run_with_buildfile_mannual(input_test_suite_addr: str, output_log_file: str, output_err_path: str,
                               output_alltest_path: str, ant_build_file_addr: str,
                               project_id: str, destfile: str,
                               version_num: int, bf_type: str, suite_num: str = "1", test_id: int = 1,
                               suite_src: str = "randoop", tmp_folder: str = TMP_ROOT_FOLDER):
    # 生成build文件
    set_build_file_mannual(project_id, version_num, output_err_path, output_alltest_path, ant_build_file_addr, destfile)
    run_inner(input_test_suite_addr=input_test_suite_addr, output_log_file=output_log_file, project_id=project_id,
              version_num=version_num, bf_type=bf_type, suite_num=suite_num, test_id=test_id,
              suite_src=suite_src, tmp_folder=tmp_folder, ant_build_file_addr=ant_build_file_addr)


def run_without_buildfile(input_test_suite_addr: str, output_log_file: str, output_err_path: str,
                          output_alltest_path: str, project_id: str, ant_build_file_addr: str,
                          version_num: int, bf_type: str, suite_num: str = "1", test_id: int = 1,
                          suite_src: str = "randoop",
                          tmp_folder: str = TMP_ROOT_FOLDER):
    # 清空build文件
    empty_build_file(output_err_path, output_alltest_path, ant_build_file_addr)
    run_inner(input_test_suite_addr=input_test_suite_addr, output_log_file=output_log_file, project_id=project_id,
              version_num=version_num, bf_type=bf_type, suite_num=suite_num,
              test_id=test_id, suite_src=suite_src, tmp_folder=tmp_folder, ant_build_file_addr=ant_build_file_addr)


def run_inner(input_test_suite_addr: str, output_log_file: str, project_id: str, version_num: int,
              bf_type: str, ant_build_file_addr: str, suite_num: str = "1", test_id: int = 1,
              suite_src: str = "randoop",
              tmp_folder: str = TMP_ROOT_FOLDER):
    # 校验参数
    is_passed = True
    if not check_proj_args(project_id, version_num, bf_type):
        is_passed = False
        sys.stderr.write("if_bash_Defects4jGenTestcase.py:项目参数验证不通过")

    if suite_src not in ["randoop", "svosuite"]:
        is_passed = False
        sys.stderr.write("if_bash_Defects4jGenTestcase.py: suite_src只能是randoop或者evosuite")

    if is_passed:
        # 执行测试用例
        run_inner_inner(input_test_suite_addr=input_test_suite_addr, output_log_file=output_log_file,
                        project_id=project_id, version_num=version_num, bf_type=bf_type,
                        suite_num=suite_num, test_id=test_id, suite_src=suite_src, tmp_folder=tmp_folder,
                        ant_build_file_addr=ant_build_file_addr)


def run_inner_inner(input_test_suite_addr: str, output_log_file: str, project_id: str, version_num: int, bf_type: str,
                    ant_build_file_addr: str, suite_num: str = "1", test_id: int = 1, suite_src: str = "randoop",
                    tmp_folder: str = TMP_ROOT_FOLDER):
    """

    :param tmp_folder:
    :param output_log_file:
    :param input_test_suite_addr  测试用例路径（该路径下需包含.java测试用例）

    :param project_id:      项目名（如Lang）
                            Generate tests for this project id. See Project module for available project IDs.
    :param version_num:     版本号 数字
    :param bf_type:         f或者b（代表fixed和buggy）
    :param suite_num:       测试集编号 代表同一个项目中不同测试集的序号 只影响测试集的存储路径
    :param test_id:         The id of the generated test suite (i.e., which run of the same configuration).
    :param suite_src:       使用的测试用例生成工具（randoop或者evosuite）
    :return:
    """
    # 删除输出文件
    file_helper.rm(output_log_file)
    cmd = ["perl", PERL_RUN_TESTCASE_WITH_JAVA_AGENT,
           "-o", output_log_file,
           "-p", project_id,
           "-b", str(version_num),
           "-x", bf_type,
           "-y", suite_num,
           "-z", str(test_id),
           "-t", tmp_folder,
           "-i", input_test_suite_addr,
           "-s", suite_src,
           "-a", ant_build_file_addr,
           ]
    # print(" ".join(cmd))
    sub_call_hook.serial(cmd)


def set_build_file(project_id: str, version_num: int, outputErrPath: str, output_alltest_path: str,
                   ant_build_file_addr: str):
    # 找到项目文件夹
    file_addr = DEFECTS4J_PROJ_INFO_ADDR + os.sep + project_id + "/loaded_classes" + os.sep + str(version_num) + ".src"
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
        outputFileAddr=ant_build_file_addr,
        javaagentArgs=agent_args,
        outputErrPath=outputErrPath,
        outputAlltestPath=output_alltest_path
    )


def set_build_file_mannual(project_id: str, destfile: str, version_num: int, outputErrPath: str,
                           output_alltest_path: str, ant_build_file_addr: str):
    agent_args = JAVAAGENT_ARGS_PREFIX + "=destfile=" + destfile + ","
    if PROJ_ROOT_PKG[project_id] != "":
        agent_args += "includes=" + PROJ_ROOT_PKG[project_id]
    # agent_args = JAVAAGENT_ARGS_PREFIX

    if_java_AntBuildFileEditor.run(
        inputFileAddr=DEFECTS4J_ANT_BUILD_TEMPLATE_ADDR,
        # outputFileAddr=DEFECTS4J_PROJ_BUILD_FILE_ADDR,
        outputFileAddr=ant_build_file_addr,
        javaagentArgs=agent_args,
        outputErrPath=outputErrPath,
        outputAlltestPath=output_alltest_path
    )


def empty_build_file(output_err_path: str, output_alltest_path: str, ant_build_file_addr: str):
    if_java_AntBuildFileEditor.run(
        inputFileAddr=DEFECTS4J_ANT_BUILD_TEMPLATE_ADDR,
        # outputFileAddr=DEFECTS4J_PROJ_BUILD_FILE_ADDR,
        outputFileAddr=ant_build_file_addr,
        javaagentArgs="$DELETE$",  # 表示删掉jvm参数
        outputErrPath=output_err_path,
        outputAlltestPath=output_alltest_path
    )


if __name__ == "__main__":
    # run_with_buildfile(
    #     # input_test_suite_addr="/tmp/xxx/Chart/mannual/1/tests",
    #     input_test_suite_addr="/tmp/xxx/Lang/mannual/1/src/test/java",
    #     output_log_file=TMP_ROOT_FOLDER + "/log.log",
    #     project_id="Lang", version_num=1, bf_type="f")
    # run_with_buildfile(
    #     input_test_suite_addr="/tmp/tmp_root_folder/Lang/Lang/randoop/1",
    #     output_log_file=TMP_ROOT_FOLDER + "/log.log",
    #     project_id="Lang", version_num=4, bf_type="f")\
    run_with_buildfile(
        input_test_suite_addr="/tmp/tmp_root_folder/xxx/middle/mannual/Lang-1-mannual/testsuite_not_reduced",
        output_log_file="/tmp/tmp_root_folder/xxx/log",
        project_id="Lang", version_num=1, bf_type="f",
        tmp_folder="/tmp/tmp_root_folder/xxx/tmp",
        output_alltest_path="/tmp/tmp_root_folder/xxx/alltests",
        output_err_path="/tmp/tmp_root_folder/xxx/err",
        ant_build_file_addr="/tmp/tmp_root_folder/xxx/ant_build_file"
    )
