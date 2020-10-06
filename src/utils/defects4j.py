"""
defects4j相关
"""
import sys

from src.CONFIG import PROJ_LIST, PROJ_VERSION_NUM


def check_proj_args(project_id: str, version_num: int, bf_type: str):
    """
    defects4j项目参数检测
    :param project_id:      项目名（如Lang）
                            Generate tests for this project id. See Project module for available project IDs.
    :param version_num:     版本号 数字
    :param bf_type:         f或者b（代表fixed和buggy）
    :return:
    """
    pass_flag = True  # 表示项目参数是否正确
    if project_id in PROJ_LIST:
        num_limit = PROJ_VERSION_NUM[project_id]
        if version_num < 1 or version_num > num_limit:
            pass_flag = False
            sys.stderr.write("不存在项目版本号:" + project_id + "-" + str(version_num) + '\n')
    else:
        pass_flag = False
        sys.stderr.write("不存在项目名:" + project_id + '\n')
    if bf_type not in ["b", "f"]:
        pass_flag = False
        sys.stderr.write("版本号后缀（bf_type）只能为b或者f:" + bf_type + '\n')

    return pass_flag


def test():
    check_proj_args("Lang", 1, "b")


if __name__ == "__main__":
    test()
