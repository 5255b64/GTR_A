"""
数据提取器
绑定一个log_parser 提取其中的数据特征
"""
import sys

from src.log_parser.log_parser import LogParser
from src.log_parser.test_class_parser import TestClass


# TODO 计算冗余信息
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
        self.redundancy_cacl_normal_base_dict = dict()      # TODO
        self.redundancy_cacl_jump_base_dict = dict()        # TODO
        self.redundancy_cacl_normal_opt_dict = dict()       # TODO
        self.redundancy_cacl_jump_opt_dict = dict()         # TODO
        self.redundancy_cas_normal_base_dict = dict()       # TODO
        self.redundancy_cas_jump_base_dict = dict()         # TODO
        self.redundancy_cas_normal_opt_dict = dict()        # TODO
        self.redundancy_cas_jump_opt_dict = dict()          # TODO
        self.redundancy_cls_normal_base_dict = dict()       # TODO
        self.redundancy_cls_jump_base_dict = dict()         # TODO
        self.redundancy_cls_normal_opt_dict = dict()        # TODO
        self.redundancy_cls_jump_opt_dict = dict()          # TODO
        self.redundancy_ss_normal_opt_dict = dict()         # TODO
        self.redundancy_ss_jump_opt_dict = dict()           # TODO

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

    def cal_redundancy_base(self, probe_obj_dict: dict, probe_all_dict: dict):
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
        # 如果测试用例没有覆盖任何桩 认为冗余为1（使用-1进行特殊判断）
        if probe_num is 0:
            return [-1, 0, 0]

        redundancy_count = probe_num
        for probe_id in probe_obj_dict.keys():
            if probe_id in probe_all_dict.keys():
                if probe_all_dict[probe_id] <= probe_obj_dict[probe_id]:
                    redundancy_count -= 1
            else:
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

    def cal_redundancy_opt(self, probe_obj_dict: dict, probe_all_dict: dict):
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

    def cal_redundancy_cacl_opt(self):
        # TODO
        test_suite = self.get_test_suite()
        for class_id in test_suite.get_test_class_dict():
            test_class = test_suite[class_id]
            for case in test_class.
        pass

    def cal_redundancy_cacl_opt_jump(self):
        # TODO
        pass

    def cal_redundancy_cacl_base(self):
        # TODO
        pass

    def cal_redundancy_cacl_base_jump(self):
        # TODO
        pass

    def cal_redundancy_cas_opt(self):
        # TODO
        pass

    def cal_redundancy_cas_opt_jump(self):
        # TODO
        pass

    def cal_redundancy_cas_base(self):
        # TODO
        pass

    def cal_redundancy_cas_base_jump(self):
        # TODO
        pass

    def cal_redundancy_cls_opt(self):
        # TODO
        pass

    def cal_redundancy_cls_opt_jump(self):
        # TODO
        pass

    def cal_redundancy_cls_base(self):
        # TODO
        pass

    def cal_redundancy_cls_base_jump(self):
        # TODO
        pass

    def cal_redundancy_ss_opt(self):
        # TODO
        pass

    def cal_redundancy_ss_opt_jump(self):
        # TODO
        pass





    def cal_redundancy_value(self, reduncancy_type:str, coverage_type:str, index_type:str):
        """

        计算CaCl指标
        :param reduncancy_type:     冗余指标类型 “BASE”或者“OPT”
        :param coverage_type:       覆盖率指标类型 “NORMAL”或者“JUMP”
        :param index_type:          指标类型 “CaCl”或者“CaS”或者“ClS”或者"SS"
        :return: dict={probe_id:CaCl_value}
        """
        flag = True
        # 输入字段校验
        if reduncancy_type not in ["BASE", "OPT"]:
            print("DataExtractor.cacl_redundancy_value:冗余指标类型只能为“BASE”或者“OPT” 错误输入-\"" + reduncancy_type + "\"", file=sys.stderr)
            flag = False
        if coverage_type not in ["NORMAL", "JUMP"]:
            print("DataExtractor.cacl_redundancy_value:覆盖率指标类型只能为“NORMAL”或者“JUMP” 错误输入-\"" + coverage_type + "\"", file=sys.stderr)
            flag = False
        if index_type not in ["CaCl", "CaS", "ClS", "SS"]:
            print("DataExtractor.cacl_redundancy_value:冗余指标类型只能为“CaCl”或者“CaS”或者“ClS”或者“SS“ 错误输入-\"" + coverage_type + "\"", file=sys.stderr)
            flag = False
        if flag:
            data_select_dict = {
                "BASE":{
                    "NORMAL":{
                        "CaCl":[self.redundancy_cacl_normal_base_dict, self.cal_redundancy_cacl_base],
                        "CaS":[self.redundancy_cas_normal_base_dict, self.cal_redundancy_cas_base],
                        "ClS":[self.redundancy_cls_normal_base_dict, self.cal_redundancy_cls_base],
                        "SS":[self.redundancy_ss_normal_opt_dict, self.cal_redundancy_opt],
                    },
                    "JUMP":{
                        "CaCl":[self.redundancy_cacl_jump_base_dict, self.cal_redundancy_cacl_base_jump],
                        "CaS":[self.redundancy_cas_jump_base_dict, self.cal_redundancy_cas_base_jump],
                        "ClS":[self.redundancy_cls_jump_base_dict, self.cal_redundancy_cls_base_jump],
                        "SS":[self.redundancy_ss_normal_opt_dict, self.cal_redundancy_ss_opt_jump],
                    },
                },
                "OPT":{
                    "NORMAL": {
                        "CaCl": [self.redundancy_cacl_normal_opt_dict, self.cal_redundancy_cacl_opt],
                        "CaS": [self.redundancy_cas_normal_opt_dict, self.cal_redundancy_cas_opt],
                        "ClS": [self.redundancy_cls_normal_opt_dict, self.cal_redundancy_cls_opt],
                        "SS": [self.redundancy_ss_normal_opt_dict, self.cal_redundancy_ss_opt],
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
            [redundancy_dict, redundancy_func] = data_select_dict[reduncancy_type][coverage_type][index_type]
            redundancy_dict.update(redundancy_func())
        else:
            return None

        return redundancy_dict

    def get_log_parser(self):
        return self.log_parser

    def get_test_suite(self):
        return self.log_parser.get_test_suite()




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
    for test_case in tc.get_case_list():
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
        for test_case in class_dict[class_id].get_test_case_list():
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
