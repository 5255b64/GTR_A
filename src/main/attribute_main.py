# TODO 重构
"""
主脚本
"""
import os
import subprocess
from src.CONFIG import RESULT_LOG_ADDR, MAIN_FOLDER, PYTHON
from src.attribute_collect import attribute_run_project
from src.utils import file_helper, logger


def run(proj_list: list, suite_src: str):
    for project_id in proj_list:
        # for project_id in PROJ_LIST:
        print("runing\t" + project_id)
        cmd = [
            PYTHON,
            MAIN_FOLDER + "/src/attribute_collect/attribute_run_project.py",
            project_id,
            suite_src
        ]
        # print(" ".join(cmd))
        out_log_addr = RESULT_LOG_ADDR + os.sep + project_id + "_stdout.log"
        err_log_addr = RESULT_LOG_ADDR + os.sep + project_id + "_stderr.log"
        file_helper.check_file_exists(out_log_addr)
        file_helper.check_file_exists(err_log_addr)
        # with open(out_log_addr, "w") as stdout:
        #     with open(err_log_addr, "w") as stderr:
        #         # 日志输出stdout和stderr
        #         subprocess.run(cmd, stdout=stdout, stderr=stderr)
        #
        #         # 控制台输出stdout和stderr
        #         # attribute_run_project.run(project_id, suite_src)

        logger.set_out(out_log_addr)
        logger.set_err(err_log_addr)
        attribute_run_project.run(project_id, suite_src)
    print("hello world")


if __name__ == "__main__":
    # main(PROJ_LIST)
    proj_list = ["Closure", "Lang", "Time", "Math", "Mockito", "Chart"]
    # proj_list = ["Math", "Mockito", "Closure"]
    # proj_list = ["Lang"]
    run(
        proj_list=proj_list,
        suite_src="mannual"
    )
    pass
