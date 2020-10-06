# TODO 重构
import glob

from interface.bash import if_bash_Defects4jCheckout, if_bash_Defects4jGenTestcase
from src.CONFIG import TMP_ROOT_FOLDER
from src.utils import sub_call_hook, file_helper


#  1）生成测试用例
#       out:   测试用例（原始）
def run(output_addr: str, tmp_root_fold: str, project_id: str, version_num: int, bf_type: str,
        suite_num: str = "1", test_id: int = 1, budget: int = 20, suite_src: str = "randoop"):
    """

    :param output_addr:     输出结果 原测试用例集的位置
    :param tmp_root_fold:                       输出文件的临时存放地址地址
    :param project_id:                          项目名（如Lang）
                                                Generate tests for this project id. See Project module for available project IDs.
    :param version_num:                         版本号 数字
    :param bf_type:                             f或者b（代表fixed和buggy）
    :param suite_num:                           测试集编号 代表同一个项目中不同测试集的序号 只影响测试集的存储路径
    :param test_id:                             The id of the generated test suite (i.e., which run of the same configuration).
    :param budget:                              生成测试用例的时间限制（秒）
                                                The time in seconds allowed for test generation.
    :param suite_src:                           使用的测试用例生成工具（randoop或者evosuite）
    :return:
    """
    tmp_fold_addr = tmp_root_fold + "/tmp_step1"
    file_helper.check_path_exists(tmp_fold_addr)

    # 生成测试用例 获得测试用例(压缩包）的地址
    zip_testcase_addr = ""

    if suite_src == "mannual":
        # 获取手工测试用例
        zip_testcase_addr = if_bash_Defects4jCheckout.run(project_id=project_id, version_num=version_num,
                                                          bf_type=bf_type, suite_num=suite_num, suite_src=suite_src,
                                                          output_addr=tmp_fold_addr)
    else:
        # 第三方工具生成测试用例
        zip_testcase_addr = if_bash_Defects4jGenTestcase.run(project_id=project_id, version_num=version_num,
                                                             bf_type=bf_type, suite_num=suite_num, test_id=test_id,
                                                             budget=budget, suite_src=suite_src,
                                                             output_addr=tmp_fold_addr)
    if str(zip_testcase_addr) == "-1":
        raise Exception("测试用例生成出错")

    # 解压出来的文件的保存地址
    unzip_file_addr = zip_testcase_addr + "/unzip_file"

    cmd = ["mkdir", "-p", unzip_file_addr]
    sub_call_hook.serial(cmd)
    # 搜索所有.bz2压缩文件 并解压
    for bz2_filename in glob.glob(zip_testcase_addr + '/*.bz2'):
        # print(bz2_filename)
        # 解压文件
        cmd = "tar -jxvf " + bz2_filename + " -C " + unzip_file_addr
        # print(cmd)
        sub_call_hook.serial_none(cmd)

    # # 保存解压出来的测试用例（原件）
    # cmd = ["rm", "-rf", output_addr]
    # sub_call_hook.serial(" ".join(cmd))
    file_helper.rm(output_addr)
    file_helper.cp(unzip_file_addr, output_addr)

    # 保存压缩的测试用例（原件）
    # cmd = ["rm", "-rf", output_addr]
    # sub_call_hook.serial(" ".join(cmd))
    # file_helper.check_path_exists(output_addr)
    # for filename in os.listdir(zip_testcase_addr):
    #     if filename.endswith("bz2"):
    #         cmd = ["mv", zip_testcase_addr +"/" + filename, output_addr + "/" + filename]
    #         sub_call_hook.serial(" ".join(cmd))


if __name__ == "__main__":
    output_unreduced_testsuite_addr = TMP_ROOT_FOLDER + "/testsuite"
    tmp_root_folder = TMP_ROOT_FOLDER

    # cmd = ["rm", "-rf", output_unreduced_testsuite_addr]
    # sub_call_hook.serial(" ".join(cmd))
    file_helper.rm(output_unreduced_testsuite_addr)

    run(output_addr=output_unreduced_testsuite_addr,
        tmp_root_fold=tmp_root_folder,
        project_id="Lang",
        version_num=1,
        bf_type="f",
        suite_src="randoop")
