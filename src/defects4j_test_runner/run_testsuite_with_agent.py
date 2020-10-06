"""
插桩 执行测试用例
得到junit日志

流程：
1）提前进行checkout
2）提前准备.bz2测试用例
3）提前生成build文件
4）调用interface进行测试用例执行 获得日志
"""

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