"""
数据提取器
绑定一个log_parser 提取其中的数据特征
"""
import sys

from CONFIG import REDUNDANCY_FUNC_TYPE, COVERAGE_TYPE, REDUNDANCY_INDEX_TYPE
from src.log_parser.log_parser import LogParser
from src.log_parser.test_class_parser import TestClass

计算冗余信息


#  （CaCl冗余）testCase相对于testClass的冗余
#  （CaS冗余）testCase相对于testSuite的冗余
#  （ClS冗余）testClass相对于testSuite的冗余
#  （SS冗余）testSuite相对于自身的冗余（只有opt）
class DataExtractor:
    def __init__(self):
        """
        成员变量:
        log_parser:LogParser                绑定的log_parser对象

        redundancy_cacl_normal_base_dict:dict       字典 存储CaCl指标 NORMAL
                                                    key为testcase_name
                                                    value为CaCl的base冗余值
        redundancy_cacl_jump_base_dict:dict         字典 存储CaCl指标 NORMAL
                                                    key为testcase_name
                                                    value为CaCl的base冗余值
        redundancy_cacl_normal_opt_dict:dict        字典 存储CaCl指标 JUMP
                                                    key为testcase_name
                                                    value为CaCl的opt冗余值
        redundancy_cacl_jump_opt_dict:dict          字典 存储CaCl指标 JUMP
                                                    key为testcase_name
                                                    value为CaCl的opt冗余值

        redundancy_cas_normal_base_dict:dict        字典 存储CaS指标 NORMAL
                                                    key为testcase_name
                                                    value为CaS的base冗余值
        redundancy_cas_jump_base_dict:dict          字典 存储CaS指标 JUMP
                                                    key为testcase_name
                                                    value为CaS的base冗余值
        redundancy_cas_normal_opt_dict:dict         字典 存储CaS指标 NORMAL
                                                    key为testcase_name
                                                    value为CaS的opt冗余值
        redundancy_cas_jump_opt_dict:dict           字典 存储CaS指标 JUMP
                                                    key为testcase_name
                                                    value为CaS的opt冗余值

        redundancy_cls_normal_base_dict:dict        字典 存储ClS指标 NORMAL
                                                    key为testclass_name
                                                    value为ClS的base冗余值
        redundancy_cls_jump_base_dict:dict          字典 存储ClS指标 JUMP
                                                    key为testclass_name
                                                    value为ClS的base冗余值
        redundancy_cls_normal_opt_dict:dict         字典 存储ClS指标 NORMAL
                                                    key为testclass_name
                                                    value为ClS的opt冗余值
        redundancy_cls_jump_opt_dict:dict           字典 存储ClS指标 JUMP
                                                    key为testclass_name
                                                    value为ClS的opt冗余值

        redundancy_ss_normal_opt_dict:dict          字典 存储SS指标 NORMAL
                                                    key为testsuite_name
                                                    value为SS的opt冗余值
        redundancy_ss_jump_opt_dict:dict            字典 存储SS指标 JUMP
                                                    key为testsuite_name
                                                    value为SS的opt冗余值
        """
        self.log_parser: LogParser = None
        self.redundancy_cacl_normal_base_dict = dict()
        self.redundancy_cacl_jump_base_dict = dict()
        self.redundancy_cacl_normal_opt_dict = dict()
        self.redundancy_cacl_jump_opt_dict = dict()
        self.redundancy_cas_normal_base_dict = dict()
        self.redundancy_cas_jump_base_dict = dict()
        self.redundancy_cas_normal_opt_dict = dict()
        self.redundancy_cas_jump_opt_dict = dict()
        self.redundancy_cls_normal_base_dict = dict()
        self.redundancy_cls_jump_base_dict = dict()
        self.redundancy_cls_normal_opt_dict = dict()
        self.redundancy_cls_jump_opt_dict = dict()
        self.redundancy_ss_normal_opt_dict = dict()
        self.redundancy_ss_jump_opt_dict = dict()

    def bind_log_parser(self, log_parser: LogParser):
        """
        绑定log_parser
        :param log_parser:
        :return:
        """
        self.log_parser = log_parser

    def parse_log(self, file: str):
        if self.log_parser is None:
            self.log_parser = LogParser()
        self.log_parser.parse_file(file)
        self.update()

    def update(self):
        self.log_parser.get_test_suite().update_probe_dict()

    def cal_redundancy_base(self, probe_obj_dict: dict, probe_all_dict: dict, isDebug: bool = False):
        """
        计算冗余指标 相对值
        probe_obj_dict 相对于 probe_all_dict 的冗余值
        计算方法：
        用probe_obj_dict减去probe_covered_dict之后 统计剩下仍不为0的probe
        仍不为0的probe越多 冗余程度就越严重

        注意：如果需要考虑NORMAL和JUMP
            在统计probe_dict时要与TestSuite.probe_inst_dict做对比
        
        :param probe_obj_dict:      目标测试用例覆盖的probe信息
        :param probe_all_dict:      相对集合覆盖的probe信息
        :return: [redundancy_value, redundancy_count, probe_num]
            redundancy_value:float  冗余值
            redundancy_count:int    冗余probe的数量
            probe_num:int           测试用例包含的probe数量
        """
        probe_num = len(probe_obj_dict)
        # 如果测试用例没有覆盖任何桩 认为冗余为1
        if probe_num is 0:
            return [1, 0, 0]

        redundancy_count = probe_num
        for probe_id in probe_obj_dict.keys():
            if probe_id in probe_all_dict.keys():
                if probe_all_dict[probe_id] <= probe_obj_dict[probe_id]:
                    redundancy_count -= 1
            else:
                if isDebug:
                    print("DataExtractor.cal_redundancy:子类覆盖信息包含父类覆盖信息所没有的probe-\"" + probe_id + "\"", file=sys.stderr)
        redundancy_value = redundancy_count / probe_num
        return [redundancy_value, redundancy_count, probe_num]

    def cal_redundancy_base_jump(self, probe_obj_dict: dict, probe_all_dict: dict):
        """
        统计分支覆盖率的cal_redundancy
        将probe_obj_dict中type为JUMP的probe单独拿出 重新构建一个probe_obj_dict
        JUMP信息 需要根据 bind 的logparser进行检索
        :param probe_obj_dict:
        :param probe_all_dict:
        :return:
        """
        probe_obj_dict_new = dict()
        probe_inst_dict = self.log_parser.get_test_suite().get_probe_inst_dict()
        for probe_id in probe_obj_dict.keys():
            if probe_inst_dict[probe_id] == "JUMP":
                probe_obj_dict_new[probe_id] = probe_obj_dict[probe_id]
        return self.cal_redundancy_base(probe_obj_dict_new, probe_all_dict)

    def cal_redundancy_opt(self, probe_obj_dict: dict, probe_all_dict: dict, isDebug: bool = False):
        """
        计算冗余指标 优化方案

        注意：如果需要考虑NORMAL和JUMP
            在统计probe_dict时要与TestSuite.probe_inst_dict做对比

        :param probe_obj_dict:      目标测试用例覆盖的probe信息
        :param probe_all_dict:      相对集合覆盖的probe信息
        :return: [redundancy_value, redundancy_count, probe_num]
            redundancy_value:float  冗余值
            redundancy_count:int    冗余probe的数量
            probe_num:int           测试用例包含的probe数量
        """
        probe_num = len(probe_obj_dict)
        # 如果测试用例没有覆盖任何桩 认为冗余为1
        if probe_num is 0:
            return [1, 0, 0]

        redundancy_count = probe_num
        for probe_id in probe_obj_dict.keys():
            if probe_id in probe_all_dict.keys():
                redundancy_count -= probe_obj_dict[probe_id] / probe_all_dict[probe_id]
            else:
                if isDebug:
                    print("DataExtractor.cal_redundancy:子类覆盖信息包含父类覆盖信息所没有的probe-\"" + probe_id + "\"", file=sys.stderr)
        redundancy_value = redundancy_count / probe_num
        return [redundancy_value, redundancy_count, probe_num]

    def cal_redundancy_opt_jump(self, probe_obj_dict: dict, probe_all_dict: dict):
        """
        统计分支覆盖率的cal_redundancy
        将probe_obj_dict中type为JUMP的probe单独拿出 重新构建一个probe_obj_dict
        JUMP信息 需要根据 bind 的logparser进行检索
        :param probe_obj_dict:
        :param probe_all_dict:
        :return:
        """
        probe_obj_dict_new = dict()
        probe_inst_dict = self.log_parser.get_test_suite().get_probe_inst_dict()
        for probe_id in probe_obj_dict.keys():
            if probe_inst_dict[probe_id] == "JUMP":
                probe_obj_dict_new[probe_id] = probe_obj_dict[probe_id]
        return self.cal_redundancy_opt(probe_obj_dict_new, probe_all_dict)

    def cal_redundancy_cacl(self, cal_redundancy_func):
        """
        计算CaCl指标的核心代码
        收集case和class的数据
        使用cal_redundancy_func进行计算
        :param cal_redundancy_func:
        :return:
        """
        result = dict()
        test_suite = self.get_test_suite()
        class_dict = test_suite.get_test_class_dict()
        for class_id in class_dict:
            test_class = class_dict[class_id]
            probe_all_dict = test_class.get_probe_dict()
            test_case_dict = test_class.get_test_case_dict()
            for case_id in test_case_dict.keys():
                case = test_case_dict[case_id]
                probe_obj_dict = case.get_probe_dict()
                result[case_id] = cal_redundancy_func(probe_obj_dict, probe_all_dict)
        return result

    def cal_redundancy_cacl_opt_normal(self):
        return self.cal_redundancy_cacl(self.cal_redundancy_opt)

    def cal_redundancy_cacl_opt_jump(self):
        return self.cal_redundancy_cacl(self.cal_redundancy_opt_jump)

    def cal_redundancy_cacl_base_normal(self):
        return self.cal_redundancy_cacl(self.cal_redundancy_base)

    def cal_redundancy_cacl_base_jump(self):
        return self.cal_redundancy_cacl(self.cal_redundancy_base_jump)

    def cal_redundancy_cas(self, cal_redundancy_func):
        """
        计算CaS指标的核心代码
        收集case和suite的数据
        使用cal_redundancy_func进行计算
        :param cal_redundancy_func:
        :return:
        """
        result = dict()
        test_suite = self.get_test_suite()
        probe_all_dict = test_suite.get_probe_dict()
        class_dict = test_suite.get_test_class_dict()
        for class_id in class_dict:
            test_class = class_dict[class_id]
            test_case_dict = test_class.get_test_case_dict()
            for case_id in test_case_dict.keys():
                case = test_case_dict[case_id]
                probe_obj_dict = case.get_probe_dict()
                result[case_id] = cal_redundancy_func(probe_obj_dict, probe_all_dict)
        return result

    def cal_redundancy_cas_opt_normal(self):
        return self.cal_redundancy_cas(self.cal_redundancy_opt)

    def cal_redundancy_cas_opt_jump(self):
        return self.cal_redundancy_cas(self.cal_redundancy_opt_jump)

    def cal_redundancy_cas_base_normal(self):
        return self.cal_redundancy_cas(self.cal_redundancy_base)

    def cal_redundancy_cas_base_jump(self):
        return self.cal_redundancy_cas(self.cal_redundancy_base_jump)

    def cal_redundancy_cls(self, cal_redundancy_func):
        """
        计算ClS指标的核心代码
        收集class和suite的数据
        使用cal_redundancy_func进行计算
        :param cal_redundancy_func:
        :return:
        """
        result = dict()
        test_suite = self.get_test_suite()
        probe_all_dict = test_suite.get_probe_dict()
        class_dict = test_suite.get_test_class_dict()
        for class_id in class_dict:
            test_class = class_dict[class_id]
            probe_obj_dict = test_class.get_probe_dict()
            result[class_id] = cal_redundancy_func(probe_obj_dict, probe_all_dict)
        return result

    def cal_redundancy_cls_opt_normal(self):
        return self.cal_redundancy_cls(self.cal_redundancy_opt)

    def cal_redundancy_cls_opt_jump(self):
        return self.cal_redundancy_cls(self.cal_redundancy_opt_jump)

    def cal_redundancy_cls_base_normal(self):
        return self.cal_redundancy_cls(self.cal_redundancy_base)

    def cal_redundancy_cls_base_jump(self):
        return self.cal_redundancy_cls(self.cal_redundancy_base_jump)

    def cal_redundancy_ss(self, cal_redundancy_func):
        """
        计算SS指标的核心代码
        收集suite的数据
        使用cal_redundancy_func进行计算
        :param cal_redundancy_func:
        :return:
        """
        result = dict()
        test_suite = self.get_test_suite()
        probe_all_dict = test_suite.get_probe_dict()
        probe_obj_dict = probe_all_dict
        result["suite"] = cal_redundancy_func(probe_obj_dict, probe_all_dict)
        return result

    def cal_redundancy_ss_opt_normal(self):
        return self.cal_redundancy_ss(self.cal_redundancy_base)

    def cal_redundancy_ss_opt_jump(self):
        return self.cal_redundancy_ss(self.cal_redundancy_base_jump)

    def cal_redundancy_value(self, redundancy_func_type: str, coverage_type: str, redundancy_index_type: str,
                             isDebug: bool = False):
        """

        计算CaCl指标
        :param redundancy_func_type:        冗余指标方法类型 “BASE”或者“OPT”
        :param coverage_type:               覆盖率指标类型 “NORMAL”或者“JUMP”
        :param redundancy_index_type:                  冗余指标范围指标类型 “CaCl”或者“CaS”或者“ClS”或者"SS"
        :return: dict={probe_id:CaCl_value}
        """
        flag = True
        # 输入字段校验
        if redundancy_func_type not in REDUNDANCY_FUNC_TYPE:
            print(
                "DataExtractor.cacl_redundancy_value:冗余指标方法类型只能为 ", REDUNDANCY_FUNC_TYPE,
                " 错误输入-\"" + redundancy_func_type + "\"",
                file=sys.stderr)
            flag = False
        if coverage_type not in COVERAGE_TYPE:
            print("DataExtractor.cacl_redundancy_value:覆盖率指标类型只能为 ", COVERAGE_TYPE, " 错误输入-\"" + coverage_type + "\"",
                  file=sys.stderr)
            flag = False
        if redundancy_index_type not in REDUNDANCY_INDEX_TYPE:
            print(
                "DataExtractor.cacl_redundancy_value:冗余指标范围类型只能为 ", REDUNDANCY_INDEX_TYPE,
                " 错误输入-\"" + coverage_type + "\"",
                file=sys.stderr)
            flag = False
        if flag:
            data_select_dict = {
                "BASE": {
                    "NORMAL": {
                        "CaCl": [self.redundancy_cacl_normal_base_dict, self.cal_redundancy_cacl_base_normal],
                        "CaS": [self.redundancy_cas_normal_base_dict, self.cal_redundancy_cas_base_normal],
                        "ClS": [self.redundancy_cls_normal_base_dict, self.cal_redundancy_cls_base_normal],
                        "SS": [self.redundancy_ss_normal_opt_dict, self.cal_redundancy_ss_opt_normal],
                    },
                    "JUMP": {
                        "CaCl": [self.redundancy_cacl_jump_base_dict, self.cal_redundancy_cacl_base_jump],
                        "CaS": [self.redundancy_cas_jump_base_dict, self.cal_redundancy_cas_base_jump],
                        "ClS": [self.redundancy_cls_jump_base_dict, self.cal_redundancy_cls_base_jump],
                        "SS": [self.redundancy_ss_normal_opt_dict, self.cal_redundancy_ss_opt_jump],
                    },
                },
                "OPT": {
                    "NORMAL": {
                        "CaCl": [self.redundancy_cacl_normal_opt_dict, self.cal_redundancy_cacl_opt_normal],
                        "CaS": [self.redundancy_cas_normal_opt_dict, self.cal_redundancy_cas_opt_normal],
                        "ClS": [self.redundancy_cls_normal_opt_dict, self.cal_redundancy_cls_opt_normal],
                        "SS": [self.redundancy_ss_normal_opt_dict, self.cal_redundancy_ss_opt_normal],
                    },
                    "JUMP": {
                        "CaCl": [self.redundancy_cacl_jump_opt_dict, self.cal_redundancy_cacl_opt_jump],
                        "CaS": [self.redundancy_cas_jump_opt_dict, self.cal_redundancy_cas_opt_jump],
                        "ClS": [self.redundancy_cls_jump_opt_dict, self.cal_redundancy_cls_opt_jump],
                        "SS": [self.redundancy_ss_normal_opt_dict, self.cal_redundancy_ss_opt_jump],
                    },
                },
            }
            # 选定存储数据的字典 和 计算冗余的方法
            [redundancy_dict, redundancy_func] = data_select_dict[redundancy_func_type][coverage_type][
                redundancy_index_type]
            temp_dict = redundancy_func()
            redundancy_dict.update(temp_dict)
        else:
            return None

        return redundancy_dict

    def get_log_parser(self):
        return self.log_parser

    def get_test_suite(self):
        return self.log_parser.get_test_suite()

    def print_summary(self):
        test_suite = self.get_test_suite()
        print("suite_inst_probe_num\t", len(test_suite.get_probe_inst_dict()))
        print("suite_cover_probe_num\t", len(test_suite.get_probe_dict()))
        print("class_cover_probe_num:")
        class_probe_counter = 0
        class_dict = test_suite.get_test_class_dict()
        for class_id in class_dict:
            test_class = class_dict[class_id]
            print("\t", len(test_class.get_probe_dict()))
            class_probe_counter += len(test_class.get_probe_dict())
            test_case_dict = test_class.get_test_case_dict()
            for case_id in test_case_dict.keys():
                case = test_case_dict[case_id]

        print("class_cover_probe_num_all\t", class_probe_counter)


def test_class_data_extractor():
    tc = TestClass()
    tc.parse_line("ACCURATE_PROBE probe_id_0")
    tc.parse_line("TESTCASE org.jfree.chart.annotations.junit.CategoryTextAnnotationTests.testHashcode")
    tc.parse_line("TESTCASE org.jfree.chart.annotations.junit.XYBoxAnnotationTests.testDrawWithNullInfo")
    tc.parse_line("ACCURATE_PROBE probe_id_0")
    tc.parse_line("ACCURATE_PROBE probe_id_1")
    tc.parse_line("ACCURATE_PROBE probe_id_2")
    tc.parse_line("ACCURATE_PROBE probe_id_3")
    tc.parse_line("TESTCASE org.jfree.chart.annotations.junit.CategoryTextAnnotationTests.testEquals")
    tc.parse_line("TESTCASE org.jfree.chart.annotations.junit.TextAnnotationTests.testHashCode")
    tc.parse_line("ACCURATE_PROBE probe_id_0")
    tc.parse_line("ACCURATE_PROBE probe_id_1")
    tc.parse_line("ACCURATE_PROBE probe_id_2")
    tc.parse_line("ACCURATE_PROBE probe_id_4")
    tc.update_probe_dict()
    print(tc.to_string())
    print(tc.get_probe_dict())
    for test_case in tc.get_case_dict():
        obj_dict = test_case.get_probe_dict()
        all_dict = tc.get_probe_dict()
        redundancy = DataExtractor.cal_redundancy_base(None, obj_dict, all_dict)
        print(test_case.get_name())
        print(redundancy)


def test_log_parser_data_extractor():
    file_addr = "/run/media/gx/仓库/GTR_A/out/log/manual/Lang/1.log"
    log_parser = LogParser()
    log_parser.parse_file(file_addr)
    log_parser.update_probe_dict()
    de = DataExtractor()
    de.bind_log_parser(log_parser)
    # print(log_parser.to_string())
    ts = log_parser.get_test_suite()
    all_dict = ts.get_probe_dict()
    class_dict = ts.get_test_class_dict()
    for class_id in class_dict.keys():
        for test_case in class_dict[class_id].get_test_case_dict().values():
            obj_dict = test_case.get_probe_dict()
            # redundancy = de.cal_redundancy_opt(obj_dict, all_dict)
            # redundancy = de.cal_redundancy_opt_jump(obj_dict, all_dict)
            redundancy = de.cal_redundancy_base(obj_dict, all_dict)
            # redundancy = de.cal_redundancy_jump(obj_dict, all_dict)
            print(test_case.get_name())
            print(redundancy)


if __name__ == "__main__":
    # test_class_data_extractor()
    test_log_parser_data_extractor()
