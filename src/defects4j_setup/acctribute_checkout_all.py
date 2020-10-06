# TODO 重构
"""
主脚本
"""
import os
import traceback

from src.CONFIG import PROJ_BUG_NUM_DICT, CHECKOUT_ROOT_FOLDER
from interface.bash import if_bash_Defects4jCheckout
from src.utils import logger


def run(proj_list: list, suite_src: str):
    for project_id in proj_list:
        # for project_id in PROJ_LIST:
        print("checkout\t" + project_id)

        attribute_checkout_project(project_id, suite_src)
    print("hello world")


def attribute_checkout_project(project_id, suite_src):
    if suite_src not in ["randoop", "evosuite", "mannual"]:
        print("Error")
        return
    for version_num in range(1, PROJ_BUG_NUM_DICT[project_id] + 1):
        output_addr = CHECKOUT_ROOT_FOLDER + os.sep + project_id + os.sep + "tmp_" + project_id + "_" + str(
            version_num) + os.sep + "tmp_step2"
        try:
            if os.path.exists(output_addr):
                print("已存在checkout:\t"+output_addr)
                continue
            if_bash_Defects4jCheckout.run(
                project_id=project_id,
                version_num=version_num,
                bf_type="f",
                output_addr=output_addr,
                suite_src=suite_src
            )
        except Exception:
            # 其实checkout过程中
            # 即使fail了也不会报Exception
            # 所以以下代码不会被执行
            # traceback.print_exc()
            logger.err(traceback.format_exc())
            print("Exception")


if __name__ == "__main__":
    """
    checkout
    注：对同一个项目连续checkout 可能出错
    """
    proj_list = ["Mockito", "Closure", "Chart", "Lang", "Time", "Math"]
    # proj_list = ["Math"]
    run(
        proj_list=proj_list,
        suite_src="mannual"
    )
    pass
