import multiprocessing
import os
import time

from src.CONFIG import NUM_PROCESS_ATTRITUBE_CASE_LEVEL, \
    PROJ_CLASSES_ADDR_LIST, PROJ_SOURCE_ADDR_LIST, JACOCO_RETRY_TIME_MAX, DEBUG_ROOT_FOLDER
from interface.perl import if_perl_RunTestcasesWithJavaagent
from interface.java import if_jar_jacococli
from interface.bash import if_bash_RunMannualSingleCaseWithJavaAgent, if_bash_RunMannualCase
from src.utils import file_helper, jacoco_html_analyzer, logger


class TestcasePool():
    def __init__(self):
        self.__pool: list = list()
        self.__is_lock: bool = False

    def add(self, obj):
        while self.__is_lock:
            time.sleep(1)
        self.__is_lock = True
        # self.__pool.append(obj)   # 加到末尾
        self.__pool.insert(0, obj)  # 加到开头
        self.__is_lock = False

    def remove(self, obj):
        while self.__is_lock:
            time.sleep(1)
        self.__is_lock = True
        try:
            self.__pool.remove(obj)
        except(Exception):
            pass
        self.__is_lock = False

    def get_obj(self):
        while self.__is_lock:
            time.sleep(1)
        self.__is_lock = True
        result = self.__pool.pop()
        self.__is_lock = False
        return result

    def is_empty(self):
        return len(self.__pool) is 0

    def get_pool(self):
        return self.__pool


# 全局测试用例池 保存未产生有效结果的测试用例
global_testcase_todo_pool = TestcasePool()
global_testcase_running_pool = TestcasePool()


def fun_process(output_failtest_addr: str, output_file_name: str, testcase_name: str, project_id: str, version_num: int,
                bf_type: str, checkout_addr: str, tmp_process_folder_addr: str, counter: int, retry_counter: int):
    """

    :param retry_counter:               重试次数
    :param counter:                     和输出文件名有关
    :param output_failtest_addr:
    :param output_file_name:
    :param testcase_name:
    :param project_id:
    :param version_num:
    :param bf_type:
    :param checkout_addr:
    :param tmp_process_folder_addr:
    :return:  boolean, testcase_name, output_failtest_addr
                boolean 表示是否执行成功
                testcase_name 测试用例名
                output_failtest_addr 表示执行失败时写入目标文件
    """
    suite_src = "mannual"
    version_name = project_id + "-" + str(version_num) + "-" + suite_src

    try:
        if not os.path.exists(output_file_name) or not os.path.isfile(output_file_name):
            # 先将checkout复制一遍
            # tmp_checkout_addr = tmp_process_folder_addr + os.sep + "checkout_" + str(counter)
            # file_helper.cp(checkout_addr, tmp_checkout_addr)

            destfile_addr = tmp_process_folder_addr + "/dest.exec"
            jacoco_html_path = tmp_process_folder_addr + "/jacoco_html"
            ant_log_addr = tmp_process_folder_addr + "/ant.log"
            jacoco_result_addr = tmp_process_folder_addr + "/jacoco_result"
            ant_build_file_addr = tmp_process_folder_addr + "/ant_build_file.xml"

            temp = testcase_name.replace(")", "").replace(os.linesep, "").split("(")
            if len(temp) is not 2:
                return False, testcase_name, output_failtest_addr, counter, retry_counter
                # fun_process_callback(False, testcase_name, output_failtest_addr, counter, retry_counter)
                # return
            pkg = temp[1]
            case_name = temp[0]
            single_test = pkg + "::" + case_name
            # 预先清除某些临时文件
            # cmd = ["rm", "-rf", destfile_addr, jacoco_html_path, ant_log_addr, jacoco_result_addr]
            # sub_call_hook.serial(" ".join(cmd))
            file_helper.rm(destfile_addr)
            file_helper.rm(jacoco_html_path)
            file_helper.rm(ant_log_addr)
            file_helper.rm(jacoco_result_addr)

            # 生成 ant buiild xml file
            if_perl_RunTestcasesWithJavaagent.set_build_file_mannual(  # 对 所有 class 做插桩
                project_id=project_id,
                version_num=version_num,
                outputErrPath="/dev/null",
                output_alltest_path="/dev/null",
                ant_build_file_addr=ant_build_file_addr,
                destfile=destfile_addr,
            )

            # 执行 single_test

            # TODO
            # 有时 dest.exec 无法正确生成
            if_bash_RunMannualSingleCaseWithJavaAgent.run(
                project_id=project_id,
                version_num=version_num,
                bf_type=bf_type,
                # checkout_addr=tmp_checkout_addr,
                checkout_addr=checkout_addr,
                output_ant_log=ant_log_addr,
                # ant_build_file_addr=destfile_addr,
                ant_build_file_addr=ant_build_file_addr,
                single_test=single_test
            )

            if not os.path.exists(destfile_addr):
                logger.err(version_name + "\t" + str(counter) + "\t文件生成失败:dest.exec")
                # 保存ant输出文件 用于debug
                if not os.path.exists(ant_build_file_addr):
                    logger.err(version_name + "\t" + str(counter) + "\t文件生成失败:ant.log")
                else:
                    debug_ant_file_addr = DEBUG_ROOT_FOLDER + os.sep + project_id + os.sep + str(
                        version_num) + os.sep + str(counter) + "_ant.log"
                    # file_helper.check_file_exists(debug_ant_file_addr)
                    file_helper.cp(ant_log_addr, debug_ant_file_addr)

                return False, testcase_name, output_failtest_addr, counter, retry_counter
            # count = 0
            # while not os.path.exists(destfile_addr):
            #     if_bash_RunMannualSingleCaseWithJavaAgent.run(
            #         project_id=project_id,
            #         version_num=version_num,
            #         bf_type=bf_type,
            #         checkout_addr=checkout_addr,
            #         output_ant_log=ant_log_addr,
            #         # ant_build_file_addr=destfile_addr,
            #         ant_build_file_addr=ant_build_file_addr,
            #         single_test=single_test
            #     )
            #     count += 1
            #     logger.err(str(count) + "\t" + output_file_name)
            #     if os.path.exists(destfile_addr) or count > JACOCO_RETRY_TIME_MAX:
            #         break
            #     time.sleep(JACOCO_RETRY_TIME_DELAY)

            # 生成 jacoco html 文档
            is_source_file_correct = False
            source_file = ""
            for sour_addr in PROJ_SOURCE_ADDR_LIST:
                # source_file = tmp_checkout_addr + os.sep + sour_addr
                source_file = checkout_addr + os.sep + sour_addr
                if os.path.exists(source_file):
                    is_source_file_correct = True
                    break
            is_class_file_path_correct = False
            class_file_path = ""
            for class_addr in PROJ_CLASSES_ADDR_LIST:
                # class_file_path = tmp_checkout_addr + os.sep + class_addr
                class_file_path = checkout_addr + os.sep + class_addr
                if os.path.exists(class_file_path):
                    is_class_file_path_correct = True
                    break
            if not is_source_file_correct or not is_class_file_path_correct:
                if not is_source_file_correct:
                    logger.err(version_name + "\tSource文件路径出错:\t" + source_file)
                if not is_class_file_path_correct:
                    logger.err(version_name + "\tClass文件路径出错:\t" + source_file)
                return False, testcase_name, output_failtest_addr, counter, retry_counter

            if_jar_jacococli.run(
                report_file_path=destfile_addr,
                class_file_path=class_file_path,
                source_file=source_file,
                output_html_path=jacoco_html_path,
            )

            # 分析 jacoco html
            jacoco_html_analyzer.run(
                html_path=jacoco_html_path,
                output_addr=jacoco_result_addr,
            )

            # 存储至output文件
            with open(output_file_name, "w") as f_out:
                # 第一行写入testcase名称
                f_out.write(testcase_name)
                with open(jacoco_result_addr, "r") as f_in:
                    for testcase_name in f_in.readlines():
                        f_out.write(testcase_name)
        else:
            # logger.err("PASS\t" + output_file_name)
            pass

    except Exception:
        return False, testcase_name, output_failtest_addr, counter, retry_counter
        # fun_process_callback(False, testcase_name, output_failtest_addr, counter, retry_counter)
        # return
    finally:
        # cmd = ["rm", "-rf", tmp_process_folder_addr]
        # sub_call_hook.serial_none(" ".join(cmd))
        file_helper.rm(tmp_process_folder_addr)
        return True, testcase_name, output_failtest_addr, counter, retry_counter
        # fun_process_callback(is_success, testcase_name, output_failtest_addr, counter, retry_counter)
        # return
    # logger.err("Ending:\t" + output_file_name.split("/")[-1])


def fun_process_callback(args):
    global global_testcase_todo_pool
    global global_testcase_running_pool
    is_success, testcase_name, output_failtest_addr, counter, retry_counter = args

    global_testcase_running_pool.remove([testcase_name, counter, retry_counter])
    if not is_success:
        if retry_counter + 1 < JACOCO_RETRY_TIME_MAX:
            global_testcase_todo_pool.add([testcase_name, counter, retry_counter + 1])
            # logger.err("执行失败:\t" + str(counter) + "\t重试次数:\t" + str(retry_counter + 1) + "\t" + output_failtest_addr)
        else:
            with open(output_failtest_addr, "a") as f:
                f.write(testcase_name + os.linesep)
            logger.err("执行失败:\t" + str(counter) + "\t重试次数:\t" + str(retry_counter) + "\t" + output_failtest_addr)
    else:
        # logger.err("执行成功:\t" + str(counter) + "\t重试次数:\t" + str(retry_counter + 1) + "\t" + output_failtest_addr)
        pass


# TODO
#  使用 多进程并行
#  进程池调度
#  根据cpu、内存资源来控制进程数量
#  jvm共享cache的情况下 同一个version可以提高运行效率
def run_multiprocess(output_path: str, project_id: str, version_num: int, bf_type: str, tmp_root_folder: str,
                     checkout_folder: str, output_alltest_addr: str, output_failtest_addr: str,
                     output_failingtest_addr: str):
    """

    :param output_failingtest_addr:
    :param output_failtest_addr:
    :param output_path:
    :param checkout_folder:
    :param output_alltest_addr:
    :param project_id:
    :param version_num:
    :param bf_type:
    :param tmp_root_folder:
    :param checkout_root_folder:
    :return:
    """
    global global_testcase_todo_pool
    global global_testcase_running_pool

    # log显示参数
    suite_src = "mannaul"
    version_name = project_id + "-" + str(version_num) + "-" + suite_src

    file_helper.check_path_exists(tmp_root_folder)

    tmp_folder_addr = tmp_root_folder + "/tmp_step2"
    tmp_checkout_addr = tmp_folder_addr + "/checkout"
    checkout_folder_path = checkout_folder + "/tmp_step2/checkout"
    tmp_ant_log_addr = tmp_folder_addr + "/ant.log"
    tmp_ant_build_file_blank_addr = tmp_folder_addr + "/ant_build_file_blank.xml"
    tmp_ant_build_file_addr = tmp_folder_addr + "/ant_build_file.xml"
    tmp_junit_log_path = tmp_folder_addr + "/junit_log"
    tmp_destfile_addr = tmp_folder_addr + "/dest.exec"
    # falling_test_addr = output_path + os.sep + str(version_num)+"falling_test.txt"
    # tmp_jacoco_html_path = tmp_folder_addr + "/jacoco_html"
    # tmp_jacoco_result_addr = tmp_folder_addr + "/jacoco_result"

    # 创建/清空文件
    with open(output_failtest_addr, "w") as f:
        f.truncate()

    file_helper.check_path_exists(output_path)

    # 备份checkout
    file_helper.cp(checkout_folder_path, tmp_checkout_addr)
    # 检查是否生成alltest 若未生成 则创建checkout
    if not os.path.exists(output_alltest_addr):
        if not os.path.exists(checkout_folder_path):
            logger.err(version_name + "\tERROR\tcheckout不存在")
            return
        file_helper.cp(checkout_folder_path, tmp_checkout_addr)
        # 生成 空白 ant buiild blank xml file
        # if_perl_RunTestcasesWithJavaagent.empty_build_file(  # 不插桩
        #     output_err_path="/dev/null",
        #     output_alltest_path="/dev/null",
        #     ant_build_file_addr=tmp_ant_build_file_blank_addr,
        # )
        # 延时 保证IO输出
        # time.sleep(0.005)
        # tmp_ant_build_file_blank_addr = checkout_addr + os.sep + ".defects4j.config"
        # checkout compile 获取 alltests
        # if_bash_RunMannualCaseWithJavaAgent.run(project_id=project_id, version_num=version_num, bf_type=bf_type,
        #                                         output_checkout_path=checkout_addr, output_ant_log=tmp_ant_log_addr,
        #                                         ant_build_file_addr=tmp_ant_build_file_blank_addr)
        # 执行默认测试
        if_bash_RunMannualCase.run(
            project_id=project_id,
            version_num=version_num,
            bf_type=bf_type,
            output_checkout_path=tmp_checkout_addr,
            falling_test_addr=output_failingtest_addr
        )
        # 延时 保证IO输出
        time.sleep(0.005)

        # cmd = ["cp", checkout_addr + "/all_tests", output_alltest_addr]
        # sub_call_hook.serial(" ".join(cmd))
        file_helper.cp(tmp_checkout_addr + os.sep + "all_tests", output_alltest_addr)
    #
    # # 生成 ant buiild xml file
    # if_perl_RunTestcasesWithJavaagent.set_build_file_mannual(  # 对 所有 class 做插桩
    #     project_id=project_id,
    #     version_num=version_num,
    #     outputErrPath="/dev/null",
    #     output_alltest_path="/dev/null",
    #     ant_build_file_addr=tmp_ant_build_file_addr,
    #     destfile=tmp_destfile_addr,
    # )

    # 清空tmp_junit_log_path
    # cmd = ["rm", "-rf", tmp_junit_log_path]
    # sub_call_hook.serial(" ".join(cmd))
    file_helper.rm(tmp_junit_log_path)
    file_helper.check_path_exists(tmp_junit_log_path)

    # 进程池
    pool = multiprocessing.Pool(processes=NUM_PROCESS_ATTRITUBE_CASE_LEVEL)

    # 对 alltests 进行 single test
    with open(output_alltest_addr, "r") as f:
        test_case_name_all = f.readlines()
        counter = 0
        for test_case_name in test_case_name_all:
            test_case_name = test_case_name.replace(os.linesep, "")
            counter += 1
            global_testcase_todo_pool.add([test_case_name, counter, 0])
            # logger.out(str(counter))

            # output_file_name = output_path + os.sep + str(counter)
            # tmp_process_folder_addr = tmp_folder_addr + "/tmp_" + str(counter)
            # pool.apply_async(
            #     fun_process,
            #     (
            #         output_failtest_addr,
            #         output_file_name,
            #         test_case_name,
            #         project_id,
            #         version_num,
            #         bf_type,
            #         checkout_addr,
            #         tmp_process_folder_addr
            #     ),
            #     callback=fun_process_callback
            # )
        while not global_testcase_todo_pool.is_empty() or not global_testcase_running_pool.is_empty():
            if not global_testcase_todo_pool.is_empty():
                test_case_name, counter, retry_counter = global_testcase_todo_pool.get_obj()
                global_testcase_running_pool.add([test_case_name, counter, retry_counter])
                output_file_name = output_path + os.sep + str(counter)
                tmp_process_folder_addr = tmp_folder_addr + "/tmp_" + str(counter)
                pool.apply_async(
                    fun_process,
                    (
                        output_failtest_addr,
                        output_file_name,
                        test_case_name,
                        project_id,
                        version_num,
                        bf_type,
                        # checkout_folder_path,
                        tmp_checkout_addr,
                        tmp_process_folder_addr,
                        counter,
                        retry_counter,
                    ),
                    callback=fun_process_callback,
                )
            else:
                time.sleep(1)
    pool.close()
    pool.join()


def run(output_path: str, project_id: str, version_num: int, bf_type: str, tmp_root_folder: str,
                     checkout_folder: str, output_alltest_addr: str, output_failtest_addr: str,
                     output_failingtest_addr: str):
    """

    :param output_failingtest_addr:
    :param output_failtest_addr:
    :param output_path:
    :param checkout_folder:
    :param output_alltest_addr:
    :param project_id:
    :param version_num:
    :param bf_type:
    :param tmp_root_folder:
    :param checkout_root_folder:
    :return:
    """

    # log显示参数
    suite_src = "mannaul"
    version_name = project_id + "-" + str(version_num) + "-" + suite_src

    file_helper.check_path_exists(tmp_root_folder)

    tmp_folder_addr = tmp_root_folder + "/tmp_step2"
    tmp_checkout_addr = tmp_folder_addr + "/checkout"
    checkout_folder_path = checkout_folder + "/tmp_step2/checkout"
    tmp_ant_log_addr = tmp_folder_addr + "/ant.log"
    tmp_ant_build_file_blank_addr = tmp_folder_addr + "/ant_build_file_blank.xml"
    tmp_ant_build_file_addr = tmp_folder_addr + "/ant_build_file.xml"
    tmp_junit_log_path = tmp_folder_addr + "/junit_log"
    tmp_destfile_addr = tmp_folder_addr + "/dest.exec"
    # falling_test_addr = output_path + os.sep + str(version_num)+"falling_test.txt"
    # tmp_jacoco_html_path = tmp_folder_addr + "/jacoco_html"
    # tmp_jacoco_result_addr = tmp_folder_addr + "/jacoco_result"

    # 创建/清空文件
    with open(output_failtest_addr, "w") as f:
        f.truncate()

    file_helper.check_path_exists(output_path)

    # 备份checkout
    file_helper.cp(checkout_folder_path, tmp_checkout_addr)
    # 检查是否生成alltest 若未生成 则创建checkout
    if not os.path.exists(output_alltest_addr):
        if not os.path.exists(checkout_folder_path):
            logger.err(version_name + "\tERROR\tcheckout不存在")
            return
        file_helper.cp(checkout_folder_path, tmp_checkout_addr)
        # 执行默认测试
        if_bash_RunMannualCase.run(
            project_id=project_id,
            version_num=version_num,
            bf_type=bf_type,
            output_checkout_path=tmp_checkout_addr,
            falling_test_addr=output_failingtest_addr
        )
        # 延时 保证IO输出
        time.sleep(0.005)

        # cmd = ["cp", checkout_addr + "/all_tests", output_alltest_addr]
        # sub_call_hook.serial(" ".join(cmd))
        file_helper.cp(tmp_checkout_addr + os.sep + "all_tests", output_alltest_addr)
    #
    # # 生成 ant buiild xml file
    # if_perl_RunTestcasesWithJavaagent.set_build_file_mannual(  # 对 所有 class 做插桩
    #     project_id=project_id,
    #     version_num=version_num,
    #     outputErrPath="/dev/null",
    #     output_alltest_path="/dev/null",
    #     ant_build_file_addr=tmp_ant_build_file_addr,
    #     destfile=tmp_destfile_addr,
    # )

    # 清空tmp_junit_log_path
    # cmd = ["rm", "-rf", tmp_junit_log_path]
    # sub_call_hook.serial(" ".join(cmd))
    file_helper.rm(tmp_junit_log_path)
    file_helper.check_path_exists(tmp_junit_log_path)

    # 对 alltests 进行 single test
    with open(output_alltest_addr, "r") as f:
        test_case_name_all = f.readlines()
        counter = 0
        for test_case_name in test_case_name_all:
            test_case_name = test_case_name.replace(os.linesep, "")
            counter += 1
            global_testcase_todo_pool.add([test_case_name, counter, 0])

            test_case_name, counter, retry_counter = global_testcase_todo_pool.get_obj()
            global_testcase_running_pool.add([test_case_name, counter, retry_counter])
            output_file_name = output_path + os.sep + str(counter)
            tmp_process_folder_addr = tmp_folder_addr + "/tmp_" + str(counter)
            fun_process(
                output_failtest_addr,
                output_file_name,
                test_case_name,
                project_id,
                version_num,
                bf_type,
                tmp_checkout_addr,
                tmp_process_folder_addr,
                counter,
                retry_counter,
            )


if __name__ == "__main__":
    output_path = "/tmp/tmp_root_folder/xxx/output"
    output_alltest_path = "/tmp/tmp_root_folder/xxx/alltest"
    output_failtest_addr = "/tmp/tmp_root_folder/xxx/failtest"
    tmp_root_fold = "/tmp/tmp_root_folder/xxx/tmp"

    # cmd = ["rm", "-rf", output_path]
    # sub_call_hook.serial(" ".join(cmd))
    file_helper.rm(output_path)
    file_helper.check_path_exists(output_path)

    time_stamp = time.time()
    run_multiprocess(
        output_path=output_path,
        project_id="Time",
        version_num=1,
        bf_type="b",
        tmp_root_folder=tmp_root_fold,
        output_alltest_addr=output_alltest_path,
        output_failtest_addr=output_failtest_addr,
    )
    time_spend = time.time() - time_stamp
    logger.out("耗时\t" + '%.2fs' % time_spend)
