"""
主脚本
"""
import os

from src.CONFIG import PROJ_LIST, PROJ_VERSION_NUM, OUT_FOLDER, CHECKOUT_FOLDER, OUT_LOG_FOLDER, OUT_MUTATION_FOLDER, \
    TMP_LOG_FOLDER, OUT_TESTSUITE_FOLDER
from defects4j_test_mutator import get_mutation_report
from defects4j_test_runner import run_testsuite_with_agent
from utils import logger
import traceback


def run(proj_list: list):
    # 日志设置
    logger.set_out(TMP_LOG_FOLDER + os.sep + "stdout.log")
    logger.set_err(TMP_LOG_FOLDER + os.sep + "stderr.log")
    # 遍历
    for project_id in proj_list:
        for version_num in range(1, PROJ_VERSION_NUM[project_id] + 1):
            for suite_src in ["manual", "randoop", "evosuite"]:
                try:
                    logger_msg = project_id + "-" + str(version_num) + "-" + suite_src + "-"
                    logger.log_out(logger_msg + "测试生成-START")
                    # 执行测试用例 获取日志
                    bf_type = "b"
                    output_junit_log_addr = OUT_LOG_FOLDER + os.sep + suite_src + os.sep + project_id + os.sep + str(
                        version_num) + ".log"
                    build_file_addr = CHECKOUT_FOLDER + os.sep + project_id + os.sep + str(
                        version_num) + bf_type + os.sep + "build.xml"
                    output_checkout_addr = CHECKOUT_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type
                    output_testsuite_addr = OUT_TESTSUITE_FOLDER + os.sep + suite_src + os.sep + project_id + os.sep + str(
                        version_num)

                    run_testsuite_with_agent.run(
                        checkout_addr=output_checkout_addr,
                        testsuite_addr=output_testsuite_addr,
                        output_junit_log_addr=output_junit_log_addr,
                        tmp_build_file_addr=build_file_addr,
                        project_id=project_id,
                        version_num=version_num,
                        bf_type=bf_type,
                        suite_src=suite_src
                    )
                    logger.log_out(logger_msg + "测试生成-END")
                    # 执行变异测试
                    logger.log_out(logger_msg + "变异测试-START")
                    if suite_src == "manual":
                        bf_type = "f"
                    checkout_addr = CHECKOUT_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type
                    output_addr = OUT_MUTATION_FOLDER + os.sep + suite_src + os.sep + project_id + os.sep + str(
                        version_num)
                    if suite_src == "manual":
                        input_suite_addr = "xxx"  # (对于manual测试用例来说是不需要的）
                    else:
                        input_suite_addr = OUT_TESTSUITE_FOLDER + os.sep + suite_src + os.sep + project_id + os.sep + str(
                            version_num) + os.sep + suite_src + ".tar.bz2"
                    get_mutation_report.run(
                        input_suite_addr=input_suite_addr,
                        project_id=project_id,
                        version_num=version_num,
                        bf_type=bf_type,
                        checkout_addr=checkout_addr,
                        output_addr=output_addr,
                        suite_src=suite_src,
                    )
                    logger.log_out(logger_msg + "变异测试-END")
                except Exception:
                    logger.log_err(logger_msg + traceback.format_exc())
                    logger.log_out(logger_msg + "Exception")


if __name__ == "__main__":
    run(PROJ_LIST)
