"""
遍历 /out/extracted_data 目录
将统计结果放到同一个csv文件中
"""
import csv
import os

from src.log_parser.data_extractor import DataExtractor
from src.CONFIG import PROJ_VERSION_NUM, PROJ_LIST, OUT_LOG_FOLDER, REDUNDANCY_FUNC_TYPE, COVERAGE_TYPE, \
    REDUNDANCY_INDEX_TYPE, OUT_EXTRACTED_DATA_FOLDER, OUT_MUTATION_FOLDER, OUT_FOLDER
from src.utils import file_helper


def run(proj_list: list):
    # 输出三个文件：
    # 1）测试用例信息（测试代码行数/分支数）
    output_file_testcase_info = OUT_FOLDER + os.sep + "testcase_info.csv"
    # 2）覆盖率信息（行覆盖率/分支覆盖率）
    output_file_coverage_info = OUT_FOLDER + os.sep + "coverage_info.csv"
    # 3）冗余信息
    output_file_redundancy_info = OUT_FOLDER + os.sep + "redundancy_info.csv"

    with open(output_file_testcase_info, 'wt') as f_testcase:
        cw_testcase = csv.writer(f_testcase, lineterminator=os.linesep)
        cw_testcase.writerow(["被测对象SUT", "manual", "manual", "randoop", "randoop", "evosuite", "evosuite"])
        cw_testcase.writerow(["被测对象SUT", "测试代码行数", "测试代码分支数", "测试代码行数", "测试代码分支数", "测试代码行数", "测试代码分支数"])
        with open(output_file_coverage_info, 'wt') as f_coverage:
            cw_coverage = csv.writer(f_coverage, lineterminator=os.linesep)
            cw_coverage.writerow(
                ["被测对象SUT", "覆盖率 coverage", "覆盖率 coverage", "覆盖率 coverage", "覆盖率 coverage", "覆盖率 coverage",
                 "覆盖率 coverage",
                 "变异分数 mutation score", "变异分数 mutation score", "变异分数 mutation score"])
            cw_coverage.writerow(
                ["被测对象SUT", "覆盖率 coverage", "覆盖率 coverage", "覆盖率 coverage", "覆盖率 coverage", "覆盖率 coverage",
                 "覆盖率 coverage",
                 "manual", "randoop", "evosuite"])
            cw_coverage.writerow(
                ["被测对象SUT", "manual", "manual", "randoop", "randoop", "evosuite", "evosuite",
                 "manual", "randoop", "evosuite"])
            cw_coverage.writerow(
                ["被测对象SUT", "行覆盖率", "分支覆盖率", "行覆盖率", "分支覆盖率", "行覆盖率", "分支覆盖率",
                 "manual", "randoop", "evosuite"])
            with open(output_file_redundancy_info, 'wt') as f_redundancy:
                cw_redundancy = csv.writer(f_redundancy, lineterminator=os.linesep)
                cw_redundancy.writerow([
                    "被测对象SUT",
                    "行覆盖指标 statement", "行覆盖指标 statement", "行覆盖指标 statement",
                    "行覆盖指标 statement", "行覆盖指标 statement", "行覆盖指标 statement",
                    "行覆盖指标 statement", "行覆盖指标 statement", "行覆盖指标 statement",
                    "行覆盖指标 statement", "行覆盖指标 statement", "行覆盖指标 statement",
                    "行覆盖指标 statement", "行覆盖指标 statement", "行覆盖指标 statement",
                    "行覆盖指标 statement", "行覆盖指标 statement", "行覆盖指标 statement",
                    "分支覆盖指标 branch", "分支覆盖指标 branch", "分支覆盖指标 branch",
                    "分支覆盖指标 branch", "分支覆盖指标 branch", "分支覆盖指标 branch",
                    "分支覆盖指标 branch", "分支覆盖指标 branch", "分支覆盖指标 branch",
                    "分支覆盖指标 branch", "分支覆盖指标 branch", "分支覆盖指标 branch",
                    "分支覆盖指标 branch", "分支覆盖指标 branch", "分支覆盖指标 branch",
                    "分支覆盖指标 branch", "分支覆盖指标 branch", "分支覆盖指标 branch",
                ])
                cw_redundancy.writerow([
                    "被测对象SUT",
                    "base指标", "base指标", "base指标", "base指标", "base指标", "base指标", "base指标", "base指标", "base指标",
                    "opt指标", "opt指标", "opt指标", "opt指标", "opt指标", "opt指标", "opt指标", "opt指标", "opt指标",
                    "base指标", "base指标", "base指标", "base指标", "base指标", "base指标", "base指标", "base指标", "base指标",
                    "opt指标", "opt指标", "opt指标", "opt指标", "opt指标", "opt指标", "opt指标", "opt指标", "opt指标",
                ])
                cw_redundancy.writerow([
                    "被测对象SUT",
                    "manual", "manual", "manual", "randoop", "randoop", "randoop", "evosuite", "evosuite", "evosuite",
                    "manual", "manual", "manual", "randoop", "randoop", "randoop", "evosuite", "evosuite", "evosuite",
                    "manual", "manual", "manual", "randoop", "randoop", "randoop", "evosuite", "evosuite", "evosuite",
                    "manual", "manual", "manual", "randoop", "randoop", "randoop", "evosuite", "evosuite", "evosuite",
                ])
                cw_redundancy.writerow([
                    "被测对象SUT",
                    "CaCl", "CaS", "ClS", "CaCl", "CaS", "ClS", "CaCl", "CaS", "ClS",
                    "CaCl", "CaS", "ClS", "CaCl", "CaS", "ClS", "CaCl", "CaS", "ClS",
                    "CaCl", "CaS", "ClS", "CaCl", "CaS", "ClS", "CaCl", "CaS", "ClS",
                    "CaCl", "CaS", "ClS", "CaCl", "CaS", "ClS", "CaCl", "CaS", "ClS",
                ])
                # 遍历
                for project_id in proj_list:
                    # for suite_src in ["manual", "randoop", "evosuite"]:
                    input_file_manual = OUT_EXTRACTED_DATA_FOLDER + os.sep + "manual" + os.sep + project_id + os.sep + "summary.csv"
                    input_file_randoop = OUT_EXTRACTED_DATA_FOLDER + os.sep + "randoop" + os.sep + project_id + os.sep + "summary.csv"
                    input_file_evosuite = OUT_EXTRACTED_DATA_FOLDER + os.sep + "evosuite" + os.sep + project_id + os.sep + "summary.csv"
                    with open(input_file_manual, 'r') as f_manual:
                        with open(input_file_randoop, 'r') as f_randoop:
                            with open(input_file_evosuite, 'r') as f_evosuite:
                                cr_manual = csv.reader(f_manual)
                                cr_randoop = csv.reader(f_randoop)
                                cr_evosuite = csv.reader(f_evosuite)
                                dict_manual = dict()
                                dict_randoop = dict()
                                dict_evosuite = dict()
                                for line in cr_manual:
                                    dict_manual[line[0]] = line[1]

                                for line in cr_randoop:
                                    dict_randoop[line[0]] = line[1]

                                for line in cr_evosuite:
                                    dict_evosuite[line[0]] = line[1]
                                # 1）保存测试用例信息（测试代码行数/分支数）
                                num_inst_statement_manual = -1
                                num_inst_statement_randoop = -1
                                num_inst_statement_evosuite = -1
                                num_inst_branch_manual = -1
                                num_inst_branch_randoop = -1
                                num_inst_branch_evosuite = -1
                                if "num_inst_statement" in dict_manual.keys():
                                    num_inst_statement_manual = dict_manual["num_inst_statement"]
                                if "num_inst_statement" in dict_randoop.keys():
                                    num_inst_statement_randoop = dict_randoop["num_inst_statement"]
                                if "num_inst_statement" in dict_evosuite.keys():
                                    num_inst_statement_evosuite = dict_evosuite["num_inst_statement"]
                                if "num_inst_branch" in dict_manual.keys():
                                    num_inst_branch_manual = dict_manual["num_inst_branch"]
                                if "num_inst_branch" in dict_randoop.keys():
                                    num_inst_branch_randoop = dict_randoop["num_inst_branch"]
                                if "num_inst_branch" in dict_evosuite.keys():
                                    num_inst_branch_evosuite = dict_evosuite["num_inst_branch"]
                                cw_testcase.writerow([
                                    project_id,
                                    num_inst_statement_manual, num_inst_branch_manual,
                                    num_inst_statement_randoop, num_inst_branch_randoop,
                                    num_inst_statement_evosuite, num_inst_branch_evosuite
                                ])
                                # 2）覆盖率信息（行覆盖率/分支覆盖率 变异分数）
                                num_covered_statement_manual = 0
                                num_covered_statement_randoop = 0
                                num_covered_statement_evosuite = 0
                                num_covered_branch_manual = 0
                                num_covered_branch_randoop = 0
                                num_covered_branch_evosuite = 0
                                mutation_score_manual = -1
                                mutation_score_randoop = -1
                                mutation_score_evosuite = -1
                                if "num_covered_statement" in dict_manual.keys() and "num_inst_statement" in dict_manual.keys():
                                    if float(dict_manual["num_inst_statement"]) > 0:
                                        num_covered_statement_manual = float(dict_manual["num_covered_statement"]) / float(dict_manual[
                                        "num_inst_statement"])
                                if "num_covered_statement" in dict_randoop.keys() and "num_inst_statement" in dict_randoop.keys():
                                    if float(dict_randoop["num_inst_statement"]) > 0:
                                        num_covered_statement_randoop = float(dict_randoop["num_covered_statement"]) / \
                                                                    float(dict_randoop["num_inst_statement"])
                                if "num_covered_statement" in dict_evosuite.keys() and "num_inst_statement" in dict_evosuite.keys():
                                    if float(dict_evosuite["num_inst_statement"]) > 0:
                                        num_covered_statement_evosuite = float(dict_evosuite["num_covered_statement"]) / \
                                                                     float(dict_evosuite["num_inst_statement"])
                                if "num_covered_branch" in dict_manual.keys() and "num_inst_statement" in dict_manual.keys():
                                    if float(dict_manual["num_inst_branch"]) > 0:
                                        num_covered_branch_manual = float(dict_manual["num_covered_branch"]) / float(dict_manual[
                                        "num_inst_branch"])
                                if "num_covered_branch" in dict_randoop.keys() and "num_inst_branch" in dict_randoop.keys():
                                    if float(dict_randoop["num_inst_branch"]) > 0:
                                        num_covered_branch_randoop = float(dict_randoop["num_covered_branch"]) / float(dict_randoop[
                                        "num_inst_branch"])
                                if "num_covered_branch" in dict_evosuite.keys() and "num_inst_branch" in dict_evosuite.keys():
                                    if float(dict_evosuite["num_inst_branch"]) > 0:
                                        num_covered_branch_evosuite = float(dict_evosuite["num_covered_branch"]) / float(dict_evosuite[
                                        "num_inst_branch"])
                                if "MutantsCovered" in dict_manual.keys() and "MutantsGenerated" in dict_manual.keys():
                                    if float(dict_manual["MutantsGenerated"]) > 0:
                                        mutation_score_manual = float(dict_manual["MutantsCovered"]) / float(dict_manual[
                                        "MutantsGenerated"])
                                if "MutantsCovered" in dict_randoop.keys() and "MutantsGenerated" in dict_randoop.keys():
                                    if float(dict_randoop["MutantsGenerated"]) > 0:
                                        mutation_score_randoop = float(dict_randoop["MutantsCovered"]) / float(dict_randoop[
                                        "MutantsGenerated"])
                                if "MutantsCovered" in dict_evosuite.keys() and "MutantsGenerated" in dict_evosuite.keys():
                                    if float(dict_evosuite["MutantsGenerated"]) > 0:
                                        mutation_score_evosuite = float(dict_evosuite["MutantsCovered"]) / float(dict_evosuite[
                                        "MutantsGenerated"])
                                # 修改 写入信息
                                cw_coverage.writerow([
                                    project_id,

                                    num_covered_statement_manual, num_covered_branch_manual,
                                    num_covered_statement_randoop, num_covered_branch_randoop,
                                    num_covered_statement_evosuite, num_covered_branch_evosuite,

                                    mutation_score_manual, mutation_score_randoop, mutation_score_evosuite
                                ])
                                # 3）冗余信息
                                manual_BASE_CaCl_NORMAL = -1
                                manual_BASE_CaS_NORMAL = -1
                                manual_BASE_ClS_NORMAL = -1
                                manual_BASE_CaCl_JUMP = -1
                                manual_BASE_CaS_JUMP = -1
                                manual_BASE_ClS_JUMP = -1
                                manual_OPT_CaCl_NORMAL = -1
                                manual_OPT_CaS_NORMAL = -1
                                manual_OPT_ClS_NORMAL = -1
                                manual_OPT_CaCl_JUMP = -1
                                manual_OPT_CaS_JUMP = -1
                                manual_OPT_ClS_JUMP = -1
                                if "BASE_CaCl_NORMAL" in dict_manual.keys():
                                    manual_BASE_CaCl_NORMAL = dict_manual["BASE_CaCl_NORMAL"]
                                if "BASE_CaS_NORMAL" in dict_manual.keys():
                                    manual_BASE_CaS_NORMAL = dict_manual["BASE_CaS_NORMAL"]
                                if "BASE_ClS_NORMAL" in dict_manual.keys():
                                    manual_BASE_ClS_NORMAL = dict_manual["BASE_ClS_NORMAL"]
                                if "BASE_CaCl_JUMP" in dict_manual.keys():
                                    manual_BASE_CaCl_JUMP = dict_manual["BASE_CaCl_JUMP"]
                                if "BASE_CaS_JUMP" in dict_manual.keys():
                                    manual_BASE_CaS_JUMP = dict_manual["BASE_CaS_JUMP"]
                                if "BASE_ClS_JUMP" in dict_manual.keys():
                                    manual_BASE_ClS_JUMP = dict_manual["BASE_ClS_JUMP"]
                                if "OPT_CaCl_NORMAL" in dict_manual.keys():
                                    manual_OPT_CaCl_NORMAL = dict_manual["OPT_CaCl_NORMAL"]
                                if "OPT_CaS_NORMAL" in dict_manual.keys():
                                    manual_OPT_CaS_NORMAL = dict_manual["OPT_CaS_NORMAL"]
                                if "OPT_ClS_NORMAL" in dict_manual.keys():
                                    manual_OPT_ClS_NORMAL = dict_manual["OPT_ClS_NORMAL"]
                                if "OPT_CaCl_JUMP" in dict_manual.keys():
                                    manual_OPT_CaCl_JUMP = dict_manual["OPT_CaCl_JUMP"]
                                if "OPT_CaS_JUMP" in dict_manual.keys():
                                    manual_OPT_CaS_JUMP = dict_manual["OPT_CaS_JUMP"]
                                if "OPT_ClS_JUMP" in dict_manual.keys():
                                    manual_OPT_ClS_JUMP = dict_manual["OPT_ClS_JUMP"]

                                randoop_BASE_CaCl_NORMAL = -1
                                randoop_BASE_CaS_NORMAL = -1
                                randoop_BASE_ClS_NORMAL = -1
                                randoop_BASE_CaCl_JUMP = -1
                                randoop_BASE_CaS_JUMP = -1
                                randoop_BASE_ClS_JUMP = -1
                                randoop_OPT_CaCl_NORMAL = -1
                                randoop_OPT_CaS_NORMAL = -1
                                randoop_OPT_ClS_NORMAL = -1
                                randoop_OPT_CaCl_JUMP = -1
                                randoop_OPT_CaS_JUMP = -1
                                randoop_OPT_ClS_JUMP = -1
                                if "BASE_CaCl_NORMAL" in dict_randoop.keys():
                                    randoop_BASE_CaCl_NORMAL = dict_randoop["BASE_CaCl_NORMAL"]
                                if "BASE_CaS_NORMAL" in dict_randoop.keys():
                                    randoop_BASE_CaS_NORMAL = dict_randoop["BASE_CaS_NORMAL"]
                                if "BASE_ClS_NORMAL" in dict_randoop.keys():
                                    randoop_BASE_ClS_NORMAL = dict_randoop["BASE_ClS_NORMAL"]
                                if "BASE_CaCl_JUMP" in dict_randoop.keys():
                                    randoop_BASE_CaCl_JUMP = dict_randoop["BASE_CaCl_JUMP"]
                                if "BASE_CaS_JUMP" in dict_randoop.keys():
                                    randoop_BASE_CaS_JUMP = dict_randoop["BASE_CaS_JUMP"]
                                if "BASE_ClS_JUMP" in dict_randoop.keys():
                                    randoop_BASE_ClS_JUMP = dict_randoop["BASE_ClS_JUMP"]
                                if "OPT_CaCl_NORMAL" in dict_randoop.keys():
                                    randoop_OPT_CaCl_NORMAL = dict_randoop["OPT_CaCl_NORMAL"]
                                if "OPT_CaS_NORMAL" in dict_randoop.keys():
                                    randoop_OPT_CaS_NORMAL = dict_randoop["OPT_CaS_NORMAL"]
                                if "OPT_ClS_NORMAL" in dict_randoop.keys():
                                    randoop_OPT_ClS_NORMAL = dict_randoop["OPT_ClS_NORMAL"]
                                if "OPT_CaCl_JUMP" in dict_randoop.keys():
                                    randoop_OPT_CaCl_JUMP = dict_randoop["OPT_CaCl_JUMP"]
                                if "OPT_CaS_JUMP" in dict_randoop.keys():
                                    randoop_OPT_CaS_JUMP = dict_randoop["OPT_CaS_JUMP"]
                                if "OPT_ClS_JUMP" in dict_randoop.keys():
                                    randoop_OPT_ClS_JUMP = dict_randoop["OPT_ClS_JUMP"]

                                evosuite_BASE_CaCl_NORMAL = -1
                                evosuite_BASE_CaS_NORMAL = -1
                                evosuite_BASE_ClS_NORMAL = -1
                                evosuite_BASE_CaCl_JUMP = -1
                                evosuite_BASE_CaS_JUMP = -1
                                evosuite_BASE_ClS_JUMP = -1
                                evosuite_OPT_CaCl_NORMAL = -1
                                evosuite_OPT_CaS_NORMAL = -1
                                evosuite_OPT_ClS_NORMAL = -1
                                evosuite_OPT_CaCl_JUMP = -1
                                evosuite_OPT_CaS_JUMP = -1
                                evosuite_OPT_ClS_JUMP = -1
                                if "BASE_CaCl_NORMAL" in dict_evosuite.keys():
                                    evosuite_BASE_CaCl_NORMAL = dict_evosuite["BASE_CaCl_NORMAL"]
                                if "BASE_CaS_NORMAL" in dict_evosuite.keys():
                                    evosuite_BASE_CaS_NORMAL = dict_evosuite["BASE_CaS_NORMAL"]
                                if "BASE_ClS_NORMAL" in dict_evosuite.keys():
                                    evosuite_BASE_ClS_NORMAL = dict_evosuite["BASE_ClS_NORMAL"]
                                if "BASE_CaCl_JUMP" in dict_evosuite.keys():
                                    evosuite_BASE_CaCl_JUMP = dict_evosuite["BASE_CaCl_JUMP"]
                                if "BASE_CaS_JUMP" in dict_evosuite.keys():
                                    evosuite_BASE_CaS_JUMP = dict_evosuite["BASE_CaS_JUMP"]
                                if "BASE_ClS_JUMP" in dict_evosuite.keys():
                                    evosuite_BASE_ClS_JUMP = dict_evosuite["BASE_ClS_JUMP"]
                                if "OPT_CaCl_NORMAL" in dict_evosuite.keys():
                                    evosuite_OPT_CaCl_NORMAL = dict_evosuite["OPT_CaCl_NORMAL"]
                                if "OPT_CaS_NORMAL" in dict_evosuite.keys():
                                    evosuite_OPT_CaS_NORMAL = dict_evosuite["OPT_CaS_NORMAL"]
                                if "OPT_ClS_NORMAL" in dict_evosuite.keys():
                                    evosuite_OPT_ClS_NORMAL = dict_evosuite["OPT_ClS_NORMAL"]
                                if "OPT_CaCl_JUMP" in dict_evosuite.keys():
                                    evosuite_OPT_CaCl_JUMP = dict_evosuite["OPT_CaCl_JUMP"]
                                if "OPT_CaS_JUMP" in dict_evosuite.keys():
                                    evosuite_OPT_CaS_JUMP = dict_evosuite["OPT_CaS_JUMP"]
                                if "OPT_ClS_JUMP" in dict_evosuite.keys():
                                    evosuite_OPT_ClS_JUMP = dict_evosuite["OPT_ClS_JUMP"]
                                cw_redundancy.writerow([
                                    project_id,
                                    manual_BASE_CaCl_NORMAL, manual_BASE_CaS_NORMAL, manual_BASE_ClS_NORMAL,
                                    randoop_BASE_CaCl_NORMAL, randoop_BASE_CaS_NORMAL, randoop_BASE_ClS_NORMAL,
                                    evosuite_BASE_CaCl_NORMAL, evosuite_BASE_CaS_NORMAL, evosuite_BASE_ClS_NORMAL,
                                    manual_OPT_CaCl_NORMAL, manual_OPT_CaS_NORMAL, manual_OPT_ClS_NORMAL,
                                    randoop_OPT_CaCl_NORMAL, randoop_OPT_CaS_NORMAL, randoop_OPT_ClS_NORMAL,
                                    evosuite_OPT_CaCl_NORMAL, evosuite_OPT_CaS_NORMAL, evosuite_OPT_ClS_NORMAL,

                                    manual_BASE_CaCl_JUMP, manual_BASE_CaS_JUMP, manual_BASE_ClS_JUMP,
                                    randoop_BASE_CaCl_JUMP, randoop_BASE_CaS_JUMP, randoop_BASE_ClS_JUMP,
                                    evosuite_BASE_CaCl_JUMP, evosuite_BASE_CaS_JUMP, evosuite_BASE_ClS_JUMP,
                                    manual_OPT_CaCl_JUMP, manual_OPT_CaS_JUMP, manual_OPT_ClS_JUMP,
                                    randoop_OPT_CaCl_JUMP, randoop_OPT_CaS_JUMP, randoop_OPT_ClS_JUMP,
                                    evosuite_OPT_CaCl_JUMP, evosuite_OPT_CaS_JUMP, evosuite_OPT_ClS_JUMP,
                                ])


if __name__ == "__main__":
    run(PROJ_LIST)
    # run(["Gson"])
