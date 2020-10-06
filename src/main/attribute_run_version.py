# TODO 重构
"""
执行单个版本的测试

1）使用script_gen_cluster.py生成聚类后的测试用例
2）使用script_get_result_data.py执行聚类后的测试用例 生成执行数据
3）使用script_gather_data.py统计执行数据

生成 覆盖率、变异分数 的数据
"""
import os
import time

from src.attribute_collect import attribute_step1_gen_test_suite_generated, \
    attribute_step2_get_junit_log_generated, \
    attribute_step3_get_err_msg, attribute_step2_get_junit_log_mannual_single
from src.utils import logger, file_helper

FIXED_BFTYPE_F = "f"
FIXED_BFTYPE_B = "b"


#  流程划分
#  1）生成测试用例
#       out:   测试用例（原始）
#  2）测试用例 插桩执行 获取插桩特征
#       in:    测试用例（原始）
#       out:  junit log文件
#  3）测试用例 执行 获取err信息
#       in:    测试用例（原始）
#       out:  err 信息文件
#  4) 聚类削减
#       in:   junit log文件
#       out:  聚类文件
#             包含bug的testcase列表文件
#  5）bug触发检测
#       in:   聚类文件+ os.sep + 包含bug的testcase列表文件
#       out:  bug触发检测结果
#  6)清除临时文件
#       在此之前 所有临时文件均不删除
#

def run(result_addr: str, middle_data_attribute_addr: str, tmp_root_folder: str, checkout_root_folder: str,
        project_id: str, version_num: int, suite_src: str):
    """

    :param result_addr:         输出结果路径 存放最终结果（三类统计数据）
    :param middle_data_attribute_addr:    保存中间生成文件 包括原测试用例集 以及保存削减信息的json文件
    :param tmp_root_folder:         中间文件存放地址
    :param checkout_root_folder:    事先存放checkout的地址

    # 可变参数
    :param project_id:
    :param version_num:
    :param suite_src:

    :return:
    """

    # log显示参数
    version_name = project_id + "-" + str(version_num) + "-" + suite_src

    # 临时存储文件目录 该目录会在某些阶段下生成 并在阶段结束时删除
    tmp_folder = tmp_root_folder + os.sep + "tmp_" + project_id + "_" + str(version_num)
    file_helper.check_path_exists(tmp_folder)
    # checkout地址
    checkout_folder = checkout_root_folder + os.sep + "tmp_" + project_id + "_" + str(version_num)

    # 需要用到的路径
    # file_helper.check_path_exists(middle_data_attribute_addr)
    # file_helper.check_path_exists(middle_data_attribute_addr+ os.sep + "/"+ os.sep + suite_src)

    file_helper.check_path_exists(
        middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name)
    minimization_result_addr = middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name + os.sep + "minimization.json"
    # 测试用例（原始）保存地址
    middle_data_testsuite_addr = middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name + os.sep + "testsuite_not_reduced"
    # junit日志文件地址
    middle_data_junit_log_addr = middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name + os.sep + "junit_log.log"
    middle_data_junit_log_no_agent_addr = middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name + os.sep + "junit_log_no_agent.log"
    # err信息文件地址
    # middle_data_err_log_addr = middle_data_addr+ os.sep + "/"+ os.sep + suite_src+ os.sep + "/"+ os.sep + version_name+ os.sep + "/err_log.log"
    middle_data_err_fixed_log_addr = middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name + os.sep + "err_fixed_log.log"
    middle_data_err_buggy_log_addr = middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name + os.sep + "err_buggy_log.log"
    # alltests文件地址
    output_alltest_path = middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name + os.sep + "alltests.log"
    # failtests文件地址
    output_failtest_addr = middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name + os.sep + "failtests.log"
    output_failingtest_addr = middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name + os.sep + "failingtest.log"
    # bug_testcases文件地址
    bug_testcases_addr = middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name + os.sep + "bug_tests.log"
    # jacoco桩信息
    middle_data_jacoco_testcase_path = middle_data_attribute_addr + os.sep + suite_src + os.sep + version_name + os.sep + "jacoco_data"
    # result 路径
    step_5_result_addr = result_addr + os.sep + project_id + os.sep + suite_src + "_" + str(version_num) + ".txt"
    file_helper.check_file_exists(step_5_result_addr)

    # 准备工作
    if os.path.exists(output_failtest_addr):
        # cmd = ["cp", "-r", output_failtest_path, output_failtest_path + ".bkb"]
        # sub_call_hook.serial(" ".join(cmd))
        file_helper.cp(output_failtest_addr, output_failtest_addr + ".bkb")
    # 杀进程
    # pycharm也是java进程
    # os.popen("ps -ef | grep java | awk '{print $2}' | xargs kill -9")
    # os.popen("ps -ef | grep ant | awk '{print $2}' | xargs kill -9")
    # os.popen("ps -ef | grep perl | awk '{print $2}' | xargs kill -9")

    # 1）生成测试用例
    #        out:   测试用例（原始）

    if suite_src != "mannual":
        time_stamp = time.time()
        attribute_step1_gen_test_suite_generated.run(
            output_addr=middle_data_testsuite_addr,
            tmp_root_fold=tmp_folder,
            project_id=project_id,
            version_num=version_num,
            bf_type=FIXED_BFTYPE_F,
            # bf_type=FIXED_BFTYPE_B,
            suite_src=suite_src)
        time_spend = time.time() - time_stamp
        logger.out(version_name + "\t" + '%.2fs' % time_spend + "\t1）生成测试用例")
    else:
        logger.out(version_name + "\tPASS\t1）生成测试用例")
        pass

    #  2）测试用例 插桩执行 获取插桩特征
    #       in:    测试用例（原始）
    #       out:  junit log文件
    time_stamp = time.time()

    # if not os.path.exists(middle_data_junit_log_addr):  # TODO edit 此处仅执行没有输出文件的部分版本

    if suite_src != "mannual":
        attribute_step2_get_junit_log_generated.run(
            input_addr=middle_data_testsuite_addr,
            output_junit_log_addr=middle_data_junit_log_addr,
            project_id=project_id,
            version_num=version_num,
            bf_type=FIXED_BFTYPE_B,
            tmp_root_folder=tmp_folder)
    else:
        # attribute_step2_get_junit_log_mannual.run(
        #     output_junit_log_addr=middle_data_junit_log_addr,
        #     project_id=project_id,
        #     version_num=version_num,
        #     bf_type=FIXED_BFTYPE_F,
        #     tmp_root_folder=tmp_folder,
        # )
        # attribute_step2_get_junit_log_mannual_single.run_multiprocess(
        attribute_step2_get_junit_log_mannual_single.run(
            output_path=middle_data_jacoco_testcase_path,
            project_id=project_id,
            version_num=version_num,
            bf_type=FIXED_BFTYPE_F,
            # bf_type=FIXED_BFTYPE_B,
            tmp_root_folder=tmp_folder,
            checkout_folder=checkout_folder,
            output_alltest_addr=output_alltest_path,
            output_failtest_addr=output_failtest_addr,
            output_failingtest_addr=output_failingtest_addr,
        )

    time_spend = time.time() - time_stamp
    logger.out(version_name + "\t" + '%.2fs' % time_spend + "\t2）测试用例 插桩执行 获取插桩特征")

    #  3）测试用例 执行 获取err信息
    #       in:    测试用例（原始）
    #       out:  err 信息文件
    #  3.1)在fixed版本上执行

    if suite_src != "mannual":
        time_stamp = time.time()
        attribute_step3_get_err_msg.run(input_addr=middle_data_testsuite_addr,
                                        project_id=project_id,
                                        version_num=version_num,
                                        bf_type=FIXED_BFTYPE_F,
                                        tmp_root_folder=tmp_folder,
                                        output_err_log_addr=middle_data_err_fixed_log_addr,
                                        output_alltest_path=output_alltest_path)

        time_spend = time.time() - time_stamp
        logger.out(
            version_name + os.sep + "\t" + os.sep + '%.2fs' % time_spend + os.sep + "\t3.1）测试用例 执行 获取err_fixed信息")
    else:
        logger.out(version_name + "\tPASS\t3.1）测试用例 执行 获取err_fixed信息")

    #  3.2)在buggy版本上执行
    if suite_src != "mannual":
        time_stamp = time.time()
        attribute_step3_get_err_msg.run(input_addr=middle_data_testsuite_addr,
                                        project_id=project_id,
                                        version_num=version_num,
                                        bf_type=FIXED_BFTYPE_B,
                                        tmp_root_folder=tmp_folder,
                                        output_err_log_addr=middle_data_err_buggy_log_addr,
                                        output_alltest_path=output_alltest_path)
        time_spend = time.time() - time_stamp
        logger.out(version_name + "\t" + '%.2fs' % time_spend + "\t3.2）测试用例 执行 获取err_buggy信息")
    else:
        logger.out(version_name + "\tPASS\t3.2）测试用例 执行 获取err_buggy信息")

    #  4) 聚类削减
    #       in:   junit log文件
    #       out:  聚类文件
    #             包含bug的testcase列表文件
    # time_stamp = time.time()
    #
    # attribute_step4_get_cluster_data.run(
    #     output_addr=minimization_result_addr,
    #     input_addr=middle_data_junit_log_addr,
    #     tmp_root_folder=tmp_folder,
    #     middle_data_err_fixed_log_addr=middle_data_err_fixed_log_addr,
    #     middle_data_err_buggy_log_addr=middle_data_err_buggy_log_addr,
    #     output_buggy_testcase_file=bug_testcases_addr
    # )
    #
    # time_spend = time.time() - time_stamp
    # logger.out(version_name+ os.sep + "\t"+ os.sep + '%.2fs' % time_spend+ os.sep + "\t4) 聚类削减")

    #  5）bug触发检测
    #       in:   聚类文件+ os.sep + 包含bug的testcase列表文件
    #       out:  bug触发检测结果
    # time_stamp = time.time()
    #
    # attribute_step5_gen_result.run(
    #     input_minimization_result_addr=minimization_result_addr,
    #     input_bug_testcase_file=bug_testcases_addr,
    #     output_result_addr=step_5_result_addr,
    #     tmp_root_folder=tmp_folder
    # )
    #
    # time_spend = time.time() - time_stamp
    # logger.out(version_name+ os.sep + "\t"+ os.sep + '%.2fs' % time_spend+ os.sep + "\t5）bug触发检测")

    # # 6)清除临时文件
    file_helper.rm(tmp_folder)


if __name__ == "__main__":
    run(
        result_addr="/tmp/tmp_root_folder/xxx/result",
        tmp_root_folder="/tmp/tmp_root_folder/xxx/tmp",
        middle_data_attribute_addr="/tmp/tmp_root_folder/xxx/middle",
        project_id="Time",
        version_num=8,
        suite_src="mannual"
    )
