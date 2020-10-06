"""
对一个项目的所有version checkout
"""
import os
import traceback

from defects4j_setup import checkout_version
from src.CONFIG import PROJ_VERSION_NUM, CHECKOUT_FOLDER, PROJ_LIST, TMP_TEST_FOLDER
from interface.bash import Defects4jCheckout
from src.utils import logger


def run(project_id: str, output_addr: str, bf_type: str = "b"):
    """

    :param project_id:      项目名 比如"Lang"
    :param output_addr:     项目输出路径 比如"tmp/Lang"
    :param bf_type:         bf_type 取值为"b"或者"f"
    :return:
    """
    output_addr_proj = output_addr
    if project_id in PROJ_LIST:
        for version_num in range(1, PROJ_VERSION_NUM[project_id] + 1):
            output_addr_version = output_addr_proj + os.sep + str(version_num) + bf_type
            checkout_version.run(project_id=project_id, version_num=version_num, bf_type=bf_type,
                                 output_addr=output_addr_version)


if __name__ == "__main__":
    project_id = "JacksonXml"
    output_addr = TMP_TEST_FOLDER + os.sep + project_id
    bf_type = "b"
    run(
        project_id=project_id,
        output_addr=output_addr,
        bf_type=bf_type
    )
