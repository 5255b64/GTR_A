from interface.perl import if_perl_RunTestcasesWithJavaagent
from interface.java import if_java_JunitLogExtractor
from interface.bash import if_bash_RunMannualCaseWithJavaAgent
from src.utils import file_helper


def run(output_junit_log_addr: str, project_id: str, version_num: int, bf_type: str, tmp_root_folder: str):
    file_helper.check_path_exists(tmp_root_folder)

    tmp_folder_addr = tmp_root_folder + "/tmp_step2"
    checkout_addr = tmp_folder_addr + "/checkout"
    tmp_ant_log_addr = tmp_folder_addr + "/ant.log"
    tmp_ant_build_file_addr = tmp_folder_addr + "/ant_build_file.xml"

    # 生成 ant buiild xml file
    if_perl_RunTestcasesWithJavaagent.set_build_file(  # 对 loaded class 做插桩
        # if_perl_RunTestcasesWithJavaagent.set_build_file_mannual(   # 对 所有 class 做插桩
        project_id=project_id,
        version_num=version_num,
        outputErrPath="/dev/null",
        output_alltest_path="/dev/null",
        ant_build_file_addr=tmp_ant_build_file_addr,
    )

    # 生成ant日志
    if_bash_RunMannualCaseWithJavaAgent.run(project_id=project_id, version_num=version_num, bf_type=bf_type,
                                            output_checkout_path=checkout_addr, output_ant_log=tmp_ant_log_addr,
                                            ant_build_file_addr=tmp_ant_build_file_addr)

    # 从ant日志中提取junit日志
    file_helper.check_file_exists(output_junit_log_addr)
    if_java_JunitLogExtractor.run(inputFileAddr=tmp_ant_log_addr, outputFileAddr=output_junit_log_addr)


if __name__ == "__main__":
    output_junit_log_addr = "/tmp/tmp_root_folder/xxx2/junit_log.log"
    file_helper.check_file_exists(output_junit_log_addr)
    tmp_root_fold = "/tmp/tmp_root_folder/xxx2/tmp"

    run(
        output_junit_log_addr=output_junit_log_addr,
        project_id="Lang", version_num=1, bf_type="f",
        tmp_root_folder=tmp_root_fold
    )
