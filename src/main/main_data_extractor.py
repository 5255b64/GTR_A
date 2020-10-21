"""
遍历 /out/log 目录
计算统计数据
将结果存放到 /out/extracted_data 目录
"""
import csv
import os

from src.log_parser.data_extractor import DataExtractor
from src.CONFIG import PROJ_VERSION_NUM, PROJ_LIST, OUT_LOG_FOLDER, REDUNDANCY_FUNC_TYPE, COVERAGE_TYPE, \
    REDUNDANCY_INDEX_TYPE, OUT_EXTRACTED_DATA_FOLDER, OUT_MUTATION_FOLDER
from src.utils import file_helper


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
    # 返回数据
    general_data_dict = dict()
    detail_data_dict = dict()
    # 读取log
    log_address = OUT_LOG_FOLDER + os.sep + suite_src + os.sep + project_id + os.sep + str(version_num) + ".log"
    # DataExtractor初始化
    data_extractor = DataExtractor()
    data_extractor.parse_log(log_address)
    test_suite = data_extractor.get_test_suite()
    # 提取version级别的数据
    for redundancy_func_type in REDUNDANCY_FUNC_TYPE:
        for coverage_type in COVERAGE_TYPE:
            for redundancy_index_type in REDUNDANCY_INDEX_TYPE:
                temp = data_extractor.cal_redundancy_value(
                    redundancy_func_type=redundancy_func_type,
                    coverage_type=coverage_type,
                    redundancy_index_type=redundancy_index_type
                )
                # temp的格式：
                # [redundancy_value, redundancy_count, probe_num]
                # redundancy_value:float  冗余值
                # redundancy_count:int    冗余probe的数量
                # probe_num:int           测试用例包含的probe数量
                signature = redundancy_func_type + "_" + redundancy_index_type + "_" + coverage_type
                # 计算冗余值
                counter = 0
                detail_dict = dict()
                for key in temp.keys():
                    counter += temp[key][0]
                    detail_dict[key] = temp[key][0]
                redundancy_value = counter / len(temp)
                # 保存冗余值
                general_data_dict[signature] = redundancy_value
                detail_data_dict[signature] = detail_dict
                # print(redundancy_func_type, redundancy_index_type, coverage_type)
                # print(redundancy_value)

    # 提取数据 行覆盖率/分支覆盖率
    # 插桩数量
    probe_inst_dict = test_suite.get_probe_inst_dict()
    probe_covered_dict = test_suite.get_probe_dict()
    # # 行覆盖率
    # # # 覆盖的代码行
    num_covered_statement = len(probe_covered_dict)
    # # # 插桩的代码行
    num_inst_statement = len(probe_inst_dict)
    # # 分支覆盖率
    # # # 覆盖的分支
    num_covered_branch = 0
    for probe_id in probe_covered_dict.keys():
        probe_type = probe_inst_dict[probe_id]
        if probe_type == "JUMP":
            num_covered_branch += 1
    # # # 插桩的分支
    num_inst_branch = 0
    for probe_type in probe_inst_dict.values():
        if probe_type == "JUMP":
            num_inst_branch += 1
    # 保存行覆盖率
    general_data_dict["num_covered_statement"] = num_covered_statement
    # 保存分支覆盖率
    general_data_dict["num_covered_branch"] = num_covered_branch
    # 保存桩行数
    general_data_dict["num_inst_statement"] = num_inst_statement
    # 保存桩分支数
    general_data_dict["num_inst_branch"] = num_inst_branch
    # print("num_covered_statement\t", num_covered_statement)
    # print("num_covered_branch\t", num_covered_branch)

    # 测试 读取变异数据
    # mutation summary.csv 格式
    # [MutantsGenerated	MutantsCovered	MutantsKilled	MutantsLive	RuntimePreprocSeconds	RuntimeAnalysisSeconds]
    mutation_summary_file = OUT_MUTATION_FOLDER + os.sep + suite_src + os.sep + project_id + os.sep + str(
        version_num) + os.sep + os.sep + suite_src + os.sep + "summary.csv"
    if os.path.exists(mutation_summary_file):
        with open(mutation_summary_file, "r") as f:
            cr = csv.reader(f)
            row = None
            for temp in cr:
                row = temp
            mutants_generated = row[0]
            mutants_covered = row[1]
            mutants_killed = row[2]
            mutants_live = row[3]

            general_data_dict["MutantsScore"] = int(mutants_killed) / int(mutants_generated)
            general_data_dict["MutantsCoverRate"] = int(mutants_covered) / int(mutants_generated)
            general_data_dict["MutantsGenerated"] = mutants_generated
            general_data_dict["MutantsCovered"] = mutants_covered
            general_data_dict["MutantsKilled"] = mutants_killed
            general_data_dict["MutantsLive"] = mutants_live
    else:
        general_data_dict["MutantsScore"] = 0
        general_data_dict["MutantsCoverRate"] = 0
        general_data_dict["MutantsGenerated"] = 0
        general_data_dict["MutantsCovered"] = 0
        general_data_dict["MutantsKilled"] = 0
        general_data_dict["MutantsLive"] = 0

    # 将general数据存储到磁盘（以csv的格式）
    out_file_folder = OUT_EXTRACTED_DATA_FOLDER + os.sep + suite_src + os.sep + project_id + os.sep + str(version_num)
    file_helper.check_path_exists(out_file_folder)
    general_file_addr = out_file_folder + os.sep + "general.csv"
    with open(general_file_addr, 'wt') as f:
        cw = csv.writer(f, lineterminator=os.linesep)
        for key in general_data_dict.keys():
            cw.writerow([key, general_data_dict[key]])

    # 将detail数据存储到磁盘
    for detail_id in detail_data_dict.keys():
        sub_detail_dict: dict = detail_data_dict[detail_id]
        detail_file_addr = out_file_folder + os.sep + detail_id + ".csv"
        with open(detail_file_addr, 'wt') as f:
            cw = csv.writer(f, lineterminator=os.linesep)
            for key in sub_detail_dict.keys():
                cw.writerow([key, sub_detail_dict[key]])

    return general_data_dict


def test_extract_all_data2():
    suite_src = "randoop"
    project_id = "Lang"
    version_num = 1
    log_address = OUT_LOG_FOLDER + os.sep + suite_src + os.sep + project_id + os.sep + str(version_num) + ".log"
    data_extractor = DataExtractor()
    data_extractor.parse_log(log_address)
    data_extractor.print_summary()
    test_suite = data_extractor.get_test_suite()
    temp1 = data_extractor.cal_redundancy_value(
        redundancy_func_type="BASE",
        coverage_type="NORMAL",
        redundancy_index_type="CaCl"
    )
    temp2 = data_extractor.cal_redundancy_value(
        redundancy_func_type="BASE",
        coverage_type="NORMAL",
        redundancy_index_type="CaS"
    )
    print("hello")


def test_extract_all_data():
    suite_src = "randoop"
    project_id = "Lang"
    version_num = 1
    extract_all_data(suite_src, project_id, version_num)


if __name__ == "__main__":
    run(PROJ_LIST)
    # test_extract_all_data()
    # test_extract_all_data2()
