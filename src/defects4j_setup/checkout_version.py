"""
为单个version做checkout
"""
import os

from CONFIG import TMP_TEST_FOLDER
from interface.bash import Defects4jCheckout


def run(project_id: str, version_num: int, bf_type: str, output_addr: str):
    """
    :param project_id:      项目名（如Lang）
                            Generate tests for this project id. See Project module for available project IDs.
    :param version_num:     版本号 数字
    :param bf_type:         f或者b（代表fixed和buggy）
    :param output_addr:     生成checkout的保存路径
    :return:
    """
    return Defects4jCheckout.run(project_id=project_id, version_num=version_num, bf_type=bf_type,
                                 output_addr=output_addr)


if __name__ == "__main__":
    project_id = "Lang"
    version_num = 1
    bf_type = "b"
    output_addr = TMP_TEST_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type
    run(project_id=project_id, version_num=version_num, bf_type=bf_type, output_addr=output_addr)
