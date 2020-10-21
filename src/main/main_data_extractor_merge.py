"""
整合每个proj的数据
"""
import csv
import os

from CONFIG import PROJ_LIST, OUT_EXTRACTED_DATA_FOLDER, PROJ_VERSION_NUM
from utils import file_helper


def run(proj_list: list):
    for project_id in proj_list:
        for suite_src in ["manual", "randoop", "evosuite"]:
            logger_msg = project_id + "-" + suite_src
            print(logger_msg)
            proj_out_data_file = OUT_EXTRACTED_DATA_FOLDER + os.sep + suite_src + os.sep + project_id + os.sep + "summary.csv"
            proj_out_data_dict = dict()
            version_num_counter = 0
            for version_num in range(1, PROJ_VERSION_NUM[project_id] + 1):
                version_general_data_file = OUT_EXTRACTED_DATA_FOLDER + os.sep + suite_src + os.sep + project_id + os.sep + str(
                    version_num) + os.sep + "general.csv"
                if os.path.exists(version_general_data_file):
                    version_num_counter += 1
                    with open(version_general_data_file, "r") as f:
                        cr = csv.reader(f)
                        for line in cr:
                            key = line[0]
                            value = line[1]
                            # 各项数值求和
                            if key not in proj_out_data_dict.keys():
                                proj_out_data_dict[key] = 0
                            proj_out_data_dict[key] += float(value)
            # 各项数值求均值
            for key in proj_out_data_dict.keys():
                proj_out_data_dict[key] /= version_num_counter

            # 保存数据
            file_helper.check_file_exists(proj_out_data_file)
            with open(proj_out_data_file, 'wt') as f:
                cw = csv.writer(f, lineterminator=os.linesep)
                for key in proj_out_data_dict.keys():
                    cw.writerow([key, proj_out_data_dict[key]])


if __name__ == "__main__":
    run(PROJ_LIST)
