"""
给定项目名称以及版本
生成对应版本的桩数据
获取聚类后的测试用例条目
生成聚类后的测试集合文件
"""

from interface.perl import if_perl_RunTestcasesWithJavaagent
from interface.java import if_java_JunitLogExtractor
from src.utils import file_helper


# TODO
#  2）测试用例 插桩执行 获取插桩特征
#       in:    测试用例（原始）
#       out:  junit log文件
def run(input_addr: str, output_junit_log_addr: str, tmp_root_folder: str, project_id: str, version_num: int,
        bf_type: str):
    """

    :param input_addr:                          原测试用例集的位置
    :param output_junit_log_addr:
    :param tmp_root_folder:                       输出文件的临时存放地址地址
    :param project_id:                          项目名（如Lang）
                                                Generate tests for this project id. See Project module for available project IDs.
    :param version_num:                         版本号 数字
    :param bf_type:                             f或者b（代表fixed和buggy）
    :return:
    """

    tmp_folder_addr = tmp_root_folder + "/tmp_step2"
    file_helper.check_path_exists(tmp_folder_addr)

    # @deplicated
    # 2.1)测试用例修改
    # 修改测试用例(包括删除flaky用例）
    # time_stamp = time.time()
    #
    # edited_testcase_addr = tmp_folder_addr + "/edited_testcase"
    # cmd = ["rm", "-rf", edited_testcase_addr]
    # sub_call_hook.serial(" ".join(cmd))
    # shutil.copytree(input_addr, edited_testcase_addr)
    # allfile = file_helper.getallfile(edited_testcase_addr)
    # for file in allfile:
    #     if file.endswith(".java"):
    #         if_java_JavaSourceCodeEditor.run(
    #             inputFileAddr=file,
    #             outputFileAddr=file
    #         )
    #
    # time_spend = time.time() - time_stamp
    # logger.out(version_name + "\t" + '%.2fs' % time_spend + "\t2.1）测试用例修改")

    # TODO delete
    edited_testcase_addr = input_addr

    # 2.2)测试用例插桩执行
    # time_stamp = time.time()

    # 使用javaagent插桩 执行测试用例 获取ant日志
    tmp_ant_log_addr = tmp_folder_addr + "/ant.log"
    tmp_folder = tmp_folder_addr + "/tmp_if_perl_RunTestcasesWithJavaagent"
    # TODO edit
    output_err_log_addr = "/dev/null"  # 不输出 err log
    output_alltest_path = "/dev/null"  # 不输出 alltests

    # # 事先创建文件 避免创建文件夹
    # f = open(tmp_ant_log_addr, 'w')
    # f.close()

    # if_perl_RunTestcasesWithJavaagent.run_with_buildfile_mannual(
    if_perl_RunTestcasesWithJavaagent.run_with_buildfile(
        input_test_suite_addr=edited_testcase_addr,
        output_log_file=tmp_ant_log_addr,
        project_id=project_id,
        version_num=version_num,
        bf_type=bf_type,
        tmp_folder=tmp_folder,
        output_err_path=output_err_log_addr,
        output_alltest_path=output_alltest_path,
        ant_build_file_addr=tmp_folder_addr + "/ant_build_file.xml"

    )
    # 从ant日志中提取junit日志
    file_helper.check_file_exists(output_junit_log_addr)
    if_java_JunitLogExtractor.run(inputFileAddr=tmp_ant_log_addr, outputFileAddr=output_junit_log_addr)

    # time_spend = time.time() - time_stamp
    # logger.out(version_name + "\t" + '%.2fs' % time_spend + "\t2.2)测试用例插桩执行")


if __name__ == "__main__":
    input_addr = "/media/gx/0226E34626E338F5/GX/Study/ECNU/TestMinimization/py_classifier_2020/out/middle_data/randoop/Math-1-randoop/testsuite_not_reduced"
    output_junit_log_addr = "/tmp/tmp_root_folder/xxx/junit_log.log"
    file_helper.check_file_exists(output_junit_log_addr)
    tmp_root_fold = "/tmp/tmp_root_folder/xxx/tmp"

    run(input_addr=input_addr,
        output_junit_log_addr=output_junit_log_addr,
        project_id="Math", version_num=1, bf_type="f",
        tmp_root_folder=tmp_root_fold)
