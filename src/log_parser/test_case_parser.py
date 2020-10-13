"""
构建TestCase类
单个testcase包含多个probe的信息
"""
import os
import sys

from src.CONFIG import TESTCASE_STR_PREFIX, PROBE_COVER_PREFIX
from src.log_parser.probe_parser import Probe


# TODO 计算冗余信息
#  （CaCl冗余）testCase相对于testClass的冗余
#  （CaS冗余）testCase相对于testSuite的冗余
class TestCase:
    def __init__(self):
        """
        TestCase类成员变量：
        test_case_name:str          测试用例名
        probe_dict:dict             该testcase包含的所有probe
                                    字典类型
                                    key为probe对象id（对象中包含type信息）
                                    # value为probe对象（包含type和被cover的次数）
                                    value固定为1
        self.ca_cl_redundancy:float （CaCl冗余）testCase相对于testClass的冗余
                                    由外部计算 并给对象赋值
        self.ca_s_redundancy:float  （CaS冗余）testCase相对于testSuite的冗余
                                    由外部计算 并给对象赋值
        """
        self.test_case_name = ""
        self.probe_dict = dict()
        self.ca_cl_redundancy = -1  # （CaCl冗余）
        self.ca_s_redundancy = -1   # （CaS冗余）

    def parse_line(self, line: str):
        tmp_list = line.replace(os.linesep, "").split(" ")
        if len(tmp_list) is 2 and tmp_list[0] == TESTCASE_STR_PREFIX:
            self.test_case_name = tmp_list[1]
        elif len(tmp_list) is 2 and tmp_list[0] == PROBE_COVER_PREFIX:
            tmp_probe = Probe()
            tmp_probe.cover_one_more_time()
            if tmp_probe.parse(line):
                self.add_probe(tmp_probe)
        else:
            print("TestCase.parse_line:字符串格式有误-\"" + line + "\"", file=sys.stderr)
            return False
        return True

    def add_probe(self, probe: Probe):
        """
        添加probe信息
        :param probe:
        :return:
        """
        probe_id = probe.get_name()
        # if probe_id in self.probe_dict.keys():
        #     self.probe_dict[probe_id].cover_one_more_time()
        # else:
        #     self.probe_dict[probe_id] = probe
        # value固定为1
        self.probe_dict[probe_id] = 1

    def get_probe_dict(self):
        return self.probe_dict

    def to_string(self):
        result = ""
        result += "\tTEST_CASE_NAME-" + self.test_case_name + os.linesep
        for probe_id in self.probe_dict:
            result += "\t\t" + probe_id + os.linesep
            # result += "\t\t" + self.probe_dict[probe_id].to_string() + os.linesep
        return result

    def get_name(self):
        return self.test_case_name

    def set_ca_cl(self, value: float):
        self.ca_cl_redundancy = value

    def set_ca_s(self, value: float):
        self.ca_s_redundancy = value

    def get_ca_cl(self):
        return self.ca_cl_redundancy

    def get_ca_s(self):
        return self.ca_s_redundancy


def test_testcase():
    tc = TestCase()
    tc.parse_line("ACCURATE_PROBE probe_id_0")
    tc.parse_line("TESTCASE org.jfree.chart.annotations.junit.XYBoxAnnotationTests.testDrawWithNullInfo")
    tc.parse_line("ACCURATE_PROBE probe_id_0")
    tc.parse_line("ACCURATE_PROBE probe_id_1")
    tc.parse_line("ACCURATE_PROBE probe_id_2")
    print(tc.to_string())
    # print(tc.probe_dict)


if __name__ == "__main__":
    test_testcase()
