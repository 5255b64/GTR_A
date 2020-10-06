# TODO 重构
"""
执行单个项目的测试

需要遍历该项目的所有版本

"""
import multiprocessing
import os
import sys
import threading
import time
import traceback

from src.CONFIG import TMP_FOLDER, PROJ_VERSION_NUM, RESULT_OUTPUT_ADDR, \
    RESULT_MIDDLE_DATA_ATTRIBUTE_PATH, CHECKOUT_FOLDER, NUM_PROCESS_ATTRITUBE_VERSION_LEVEL
from src.attribute_collect import attribute_run_version
from src.utils import logger


def fun_process(project_id: str, version_num: int, suite_src: str):
    version_name = project_id + "-" + str(version_num) + "-" + suite_src

    # 输出日志
    logger.log_out(version_name + "\tSTART")
    # logger.err(version_name + "\tSTART")

    # 超时检测机制：使用thread.join 线程阻塞 达到timeout时自动结束
    # 根据是否有有效输出 来判断是否存在超时（或者其他问题）
    tmp_root_folder = TMP_FOLDER + os.sep + project_id
    checkout_root_folder = CHECKOUT_FOLDER + os.sep + project_id

    time_stamp = time.time()
    try:
        attribute_run_version.run(
            result_addr=RESULT_OUTPUT_ADDR,
            middle_data_attribute_addr=RESULT_MIDDLE_DATA_ATTRIBUTE_PATH,
            # middle_data_analysis_addr=RESULT_MIDDLE_DATA_ANALYSIS_PATH,
            tmp_root_folder=tmp_root_folder,  # 每个项目的中间临时文件存放在不同位置 避免并行错误
            checkout_root_folder=checkout_root_folder,
            project_id=project_id,
            version_num=version_num,
            suite_src=suite_src
        )
    except(Exception):
        # traceback.print_exc()
        logger.log_err(traceback.format_exc())
        logger.log_out(version_name + "\tEXCEPTION")
    time_spend = time.time() - time_stamp
    logger.log_out(version_name + "\t运行时间:\t" + '%.2fs' % time_spend + "\ts")
    logger.log_out(version_name + "\tEND")


def run(project_id: str, suite_src: str):
    if suite_src not in ["randoop", "evosuite", "mannual"]:
        logger.log_out("suite_src必须为[\"randoop\",\"evosuite\",\"mannnual\"]\t" + suite_src)
        # logger.err("suite_src必须为[\"randoop\",\"evosuite\",\"mannnual\"]\t" + suite_src)
        return
    pool = multiprocessing.Pool(processes=NUM_PROCESS_ATTRITUBE_VERSION_LEVEL)
    for version_num in range(1, PROJ_VERSION_NUM[project_id] + 1):
        pool.apply_async(
            # TODO
            fun_process,
            (
                project_id,
                version_num,
                suite_src,
            )
        )
        # version_name = project_id + "-" + str(version_num) + "-" + suite_src
        #
        # # 输出日志
        # logger.out(version_name + "\tSTART")
        # # logger.err(version_name + "\tSTART")
        #
        # # 超时检测机制：使用thread.join 线程阻塞 达到timeout时自动结束
        # # 根据是否有有效输出 来判断是否存在超时（或者其他问题）
        # tmp_root_folder = TMP_ROOT_FOLDER + os.sep + project_id
        # checkout_root_folder = CHECKOUT_ROOT_FOLDER + os.sep + project_id
        #
        # time_stamp = time.time()
        # try:
        #     attribute_run_version.run(
        #         result_addr=RESULT_OUTPUT_ADDR,
        #         middle_data_attribute_addr=RESULT_MIDDLE_DATA_ATTRIBUTE_PATH,
        #         # middle_data_analysis_addr=RESULT_MIDDLE_DATA_ANALYSIS_PATH,
        #         tmp_root_folder=tmp_root_folder,  # 每个项目的中间临时文件存放在不同位置 避免并行错误
        #         checkout_root_folder=checkout_root_folder,
        #         project_id=project_id,
        #         version_num=version_num,
        #         suite_src=suite_src
        #     )
        # except(Exception):
        #     traceback.print_exc()
        #     logger.out(version_name + "\tEXCEPTION")
        # time_spend = time.time() - time_stamp
        # logger.out(version_name + "\t运行时间:\t" + '%.2fs' % time_spend + "\ts")
        # logger.out(version_name + "\tEND")
        # logger.err(version_name + "\tEND")
    # except Exception as e:
    #     logger.err(version_name + "\tError\t" + str(e))

    # 删除临时文件
    # tmp_file_deleter.run()
    pool.close()
    pool.join()


def run_multi_process(project_id: str, suite_src: str):
    if suite_src not in ["randoop", "evosuite", "mannual"]:
        logger.log_out("suite_src必须为[\"randoop\",\"evosuite\",\"mannnual\"]\t" + suite_src)
        # logger.err("suite_src必须为[\"randoop\",\"evosuite\",\"mannnual\"]\t" + suite_src)
        return
    for version_num in range(1, PROJ_VERSION_NUM[project_id] + 1):
        version_name = project_id + "-" + str(version_num) + "-" + suite_src

        # 输出日志
        # sys.stdout.write(
        #     str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\tRunning\t" + version_name + "\n"))
        logger.log_out(version_name + "\tSTART")
        # logger.err(version_name + "\tSTART")
        try:
            # script_run_version.run(
            #     tmp_root_folder=TMP_ROOT_FOLDER,
            #     project_id=project_id,
            #     version_num=version_num,
            #     bf_type=bf_type,
            #     suite_src=suite_src
            # )

            # 超时检测机制：使用thread.join 线程阻塞 达到timeout时自动结束
            # 根据是否有有效输出 来判断是否存在超时（或者其他问题）
            tmp_root_folder = TMP_FOLDER + os.sep + project_id

            def target():
                attribute_run_version.run(
                    result_addr=RESULT_OUTPUT_ADDR,
                    middle_data_attribute_addr=RESULT_MIDDLE_DATA_ATTRIBUTE_PATH,
                    tmp_root_folder=tmp_root_folder,  # 每个项目的中间临时文件存放在不同位置 避免并行错误
                    project_id=project_id,
                    version_num=version_num,
                    suite_src=suite_src
                )

            thread = threading.Thread(target=target)

            time_stamp = time.time()
            thread.start()
            # thread.setDaemon(True)  # (有问题 会导致多线程执行)设置守护线程 主线程结束后杀死子线程
            thread.join()
            # thread.join(SCRIPT_VERSION_TIMEOUT)
            time_spend = time.time() - time_stamp
            logger.log_out(version_name + "\t运行时间:\t" + '%.2fs' % time_spend + "\ts")
            if thread.isAlive():
                logger.log_out(version_name + "\t运行超时！！！")
        except Exception as e:
            logger.log_err(version_name + "\tError\t" + str(e))
        finally:
            logger.log_out(version_name + "\tEND")
            # logger.err(version_name + "\tEND")

        # 删除临时文件
        # tmp_file_deleter.run()


if __name__ == "__main__":
    # 注：该类通过bash被调用 需修改系统输入参数进行调试
    if len(sys.argv) < 3:
        raise Exception("参数数量不足")
    project_id = sys.argv[1]
    suite_src = sys.argv[2]
    run(project_id=project_id, suite_src=suite_src)
