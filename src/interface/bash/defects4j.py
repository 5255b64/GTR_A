"""
用于调用defects4j的脚本
"""

from src.utils import sub_call_hook
from src.CONFIG import BASH_DEFECT4J, DEFECTS4J_ADD_PATH_FILE


def run(args: str):
    cmd = ["bash", BASH_DEFECT4J, DEFECTS4J_ADD_PATH_FILE] + args.split(" ")
    # print(cmd)
    sub_call_hook.serial(cmd)


if __name__ == "__main__":
    run("-h haha")