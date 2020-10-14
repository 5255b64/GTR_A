"""
遍历 /out/log 目录
计算统计数据
将结果存放到 /out/extracted_data 目录
"""
import os

from log_parser.data_extractor import DataExtractor
from log_parser.test_suite_parser import TestSuite
from src.CONFIG import PROJ_VERSION_NUM, PROJ_LIST, OUT_LOG_FOLDER


def run(proj_list: list):
    # 遍历
    for project_id in proj_list:
        for suite_src in ["manual", "randoop", "evosuite"]:
            for version_num in range(1, PROJ_VERSION_NUM[project_id] + 1):
                logger_msg = project_id + "-" + str(version_num) + "-" + suite_src + "-"
                process_func(
                    logger_msg,
                    suite_src,
                    project_id,
                    version_num,
                )


def process_func(logger_msg: str, suite_src: str, project_id: str, version_num: int):
    """
    单个进程执行的内容
    :param logger_msg:
    :param suite_src:
    :param project_id:
    :param version_num:
    :return:
    """
    # 记录当前version是否执行完成
    flag = False
    try:
        print(logger_msg)
        extract_all_data(suite_src, project_id, version_num)
    except Exception:
        # TODO
        pass

    if flag:
        # TODO
        pass
    else:
        # TODO
        pass


def extract_all_data(suite_src: str, project_id: str, version_num: int):
    """

    :param suite_src:
    :param project_id:
    :param version_num:
    :return:
    """
    # 读取log
    log_address = OUT_LOG_FOLDER + os.sep + suite_src + os.sep + project_id + os.sep + str(version_num) + ".log"
    # TODO 提取数据
    data_extractor = DataExtractor()
    data_extractor.parse_log(log_address)
    test_suite: TestSuite = data_extractor.get_test_suite()

    # TODO 提取数据 行覆盖率/分支覆盖率
    # TODO 提取数据
    pass


if __name__ == "__main__":
    run(PROJ_LIST)
