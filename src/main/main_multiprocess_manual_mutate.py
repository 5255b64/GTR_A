"""
主脚本 多进程版本
使用进程池进行管理
"""
import multiprocessing
import os

from src.CONFIG import PROJ_LIST, PROJ_VERSION_NUM, CHECKOUT_FOLDER, OUT_LOG_FOLDER, OUT_MUTATION_FOLDER, \
    TMP_LOG_FOLDER, OUT_TESTSUITE_FOLDER, PROCESS_NUM, CONTINUE_FINISHED_FILE, CONTINUE_ERROR_FILE
from src.defects4j_test_mutator import get_mutation_report
from src.defects4j_test_runner import run_testsuite_with_agent
from src.utils import logger
import traceback

from utils import file_helper

log_continue_file = CONTINUE_FINISHED_FILE + ".temp"
log_error_file = CONTINUE_ERROR_FILE + ".temp"


def run(proj_list: list):
    # 日志设置
    # logger.set_out(TMP_LOG_FOLDER + os.sep + "stdout_tmp.log")
    # logger.set_err(TMP_LOG_FOLDER + os.sep + "stderr_tmp.log")
    # 断点续传 读取已记录的文件

    continue_finished_dict = logger.get_continue_dict(log_continue_file)
    continue_error_dict = logger.get_continue_dict(log_error_file)
    # 进程池
    # pool = multiprocessing.Pool(processes=PROCESS_NUM)
    pool = multiprocessing.Pool(processes=1)
    # 遍历
    for project_id in proj_list:
        for suite_src in ["manual"]:
            # suite_src作为第二层循环 不做最内层循环
            # 防止多个进程对同一个checkout做操作
            for version_num in range(1, PROJ_VERSION_NUM[project_id] + 1):
                logger_msg = project_id + "-" + str(version_num) + "-" + suite_src + "-"
                if logger_msg not in continue_finished_dict.keys() \
                        and logger_msg not in continue_error_dict.keys():
                    # 断点续传 判断是否续传
                    pool.apply_async(
                        process_func,
                        (
                            logger_msg,
                            suite_src,
                            project_id,
                            version_num,
                        )
                    )

    pool.close()
    pool.join()


def process_func(logger_msg: str, suite_src: str, project_id: str, version_num: int):
    # 记录当前version是否执行完成
    flag = False
    try:
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
        flag = True
    except Exception:
        logger.log_err(logger_msg + traceback.format_exc())
        logger.log_out(logger_msg + "Exception")
    # 断点续传 记录已处理的文件
    if flag:
        logger.continue_log(log_continue_file, logger_msg)
    else:
        logger.continue_log(log_error_file, logger_msg)

    # 删除checkout临时文件
    file_helper.rm(checkout_addr)


if __name__ == "__main__":
    run(PROJ_LIST)
