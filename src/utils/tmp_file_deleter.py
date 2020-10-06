# TODO 重构 忘了这个代码是做什么的
import os
import time

from src.CONFIG import SCRIPT_VERSION_TIMEOUT
from src.utils import file_helper, logger


def run():
    base_dir = "/tmp"
    tmp = os.listdir(base_dir)
    for file_name in tmp:
        if file_name.startswith("run_randoop.pl") \
                or file_name.startswith("fix_test_suite.pl") \
                or file_name.startswith("RunTestcasesWithJavaagent.pl"):
            abs_dir = base_dir + os.sep + file_name
            last_used_time_s = time.time()-os.stat(abs_dir).st_atime
            if last_used_time_s>SCRIPT_VERSION_TIMEOUT:
                file_helper.rm(abs_dir)
                logger.err("TMP FILE DELETED\t" + abs_dir)


if __name__ == "__main__":
    run()
