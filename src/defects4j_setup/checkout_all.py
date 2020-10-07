"""
对所有的项目做checkout
"""
import os

from CONFIG import PROJ_LIST, PROJ_VERSION_NUM, CHECKOUT_FOLDER
from defects4j_setup import checkout_version


def run():
    for project_id in PROJ_LIST:
        # for version_num in range(1, PROJ_VERSION_NUM[project_id] + 1):
        for version_num in range(1, 2):
            bf_type = "b"
            output_addr = CHECKOUT_FOLDER + os.sep + project_id + os.sep + str(version_num) + bf_type
            checkout_version.run(
                project_id=project_id,
                version_num=version_num,
                bf_type=bf_type,
                output_addr=output_addr
            )


if __name__ == "__main__":
    run()
