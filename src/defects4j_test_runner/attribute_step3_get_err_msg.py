"""
给定项目名称以及版本
生成对应版本的桩数据
获取聚类后的测试用例条目
生成聚类后的测试集合文件
"""

from interface.perl import if_perl_RunTestcasesWithJavaagent
from src.CONFIG import TMP_ROOT_FOLDER
from src.utils import file_helper


#  3）测试用例 执行 获取err信息
#       in:    测试用例（原始）
#       out:  err 信息文件
def run(input_addr: str, output_err_log_addr: str, output_alltest_path: str, tmp_root_folder: str, project_id: str,
        version_num: int,
        bf_type: str):
    """

    :param input_addr:                          原测试用例集的位置
    :param output_err_log_addr:
    :param tmp_root_folder:                       输出文件的临时存放地址地址
    :param project_id:                          项目名（如Lang）
                                                Generate tests for this project id. See Project module for available project IDs.
    :param version_num:                         版本号 数字
    :param bf_type:                             f或者b（代表fixed和buggy）
    :return:
    """

    tmp_folder_addr = tmp_root_folder + "/tmp_step3"
    file_helper.check_path_exists(tmp_folder_addr)

    # cmd = ["rm", "-rf", output_err_log_addr, output_alltest_path]
    # sub_call_hook.serial(" ".join(cmd))
    file_helper.rm(output_err_log_addr)
    file_helper.rm(output_alltest_path)

    edited_testcase_addr = input_addr

    # 使用javaagent插桩 执行测试用例 获取ant日志
    ant_log_addr = "/dev/null"
    tmp_folder = tmp_folder_addr + "/tmp_if_perl_RunTestcasesWithJavaagent"

    if_perl_RunTestcasesWithJavaagent.run_without_buildfile(
        input_test_suite_addr=edited_testcase_addr,
        output_log_file=ant_log_addr,
        project_id=project_id,
        version_num=version_num,
        bf_type=bf_type,
        tmp_folder=tmp_folder,
        output_err_path=output_err_log_addr,
        output_alltest_path=output_alltest_path,
        ant_build_file_addr=tmp_folder_addr + "/ant_build_file.xml"
    )


if __name__ == "__main__":
    # output_junit_log_addr = TMP_ROOT_FOLDER + "/junit_log.log"
    output_err_log_addr = TMP_ROOT_FOLDER + "/err_log.log"
    # file_helper.check_file_exists(output_junit_log_addr)
    input_addr = TMP_ROOT_FOLDER + "/testsuite"
    tmp_root_fold = TMP_ROOT_FOLDER
    output_alltest_path = TMP_ROOT_FOLDER + "/alltests.log"

    run(input_addr=input_addr,
        project_id="Closure", version_num=1, bf_type="f",
        tmp_root_folder=tmp_root_fold,
        output_err_log_addr=output_err_log_addr,
        output_alltest_path=output_alltest_path)
