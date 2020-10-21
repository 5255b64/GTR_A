"""
构建TestClass类
单个testclass包含多个testcase的信息
"""
import os
import sys

from CONFIG import TESTCASE_STR_PREFIX
from src.log_parser.test_case_parser import TestCase


# TODO 计算冗余
#  （ClS冗余）testClass相对于testSuite的冗余
class TestClass:
    def __init__(self):
        """
        TestClass类成员变量：
        test_class_name:str
        test_case_dict:list             该testclass包含的所有testcase
                                        字典类型
                                        key为case_id
                                        value为testcase
        test_case_ptr                   当前parse到的test_case的对象指针
        self.cl_s_redundancy:float      （ClS冗余）testClass相对于testSuite的冗余
                                        由外部计算 并给对象赋值
        probe_dict:dict                 当前testclass的所有probe
                                        key为probe_id
                                        value=被cover的次数
        """
        self.test_class_name = None
        self.test_case_dict = dict()
        self.test_case_ptr = None
        self.cl_s_redundancy = -1
        self.probe_dict = dict()    # probe cover info

    def parse_line(self, line, isDebug:bool=False):
        tmp_list = line.replace(os.linesep, "").split(" ")
        if len(tmp_list) is 2 and tmp_list[0] == TESTCASE_STR_PREFIX:
            test_case_name = tmp_list[1]
            test_class_name = ".".join(test_case_name.split(".")[0:-1])
            # 校验class_name 或者赋初值
            if self.test_class_name is None:
                self.test_class_name = test_class_name
            elif self.test_class_name != test_class_name:
                if isDebug:
                    print("TestClass.parse_line:class发生改变-\"" + line + "\"", file=sys.stderr)
                return False
            # 判断是否是新的test_case
            if self.test_case_ptr is None or test_case_name != self.test_case_ptr.get_name():
                # 新的test_case
                self.test_case_ptr = TestCase()
                self.test_case_ptr.parse_line(line)     # TestCase对象要记录case_name
                # self.test_case_dict.append(self.test_case_ptr))   #
                self.test_case_dict[self.test_case_ptr.get_name()] = self.test_case_ptr
        # 旧的test_case
        if self.test_case_ptr is not None:
            self.test_case_ptr.parse_line(line)
        else:
            if isDebug:
                print("TestClass.parse_line:testcase为None的情况下发现Probe-\"" + line + "\"", file=sys.stderr)
            return False
        return True

    def set_name(self, name: str):
        self.test_class_name = name

    def add_case(self, test_case: TestCase):
        # self.test_case_dict.append(test_case)
        self.test_case_dict[test_case.get_name()] = test_case

    def get_name(self):
        return self.test_class_name

    def get_case_dict(self):
        return self.test_case_dict

    def to_string(self):
        result = ""
        result += "TEST_CLASS_NAME-" + self.test_class_name+os.linesep
        for testcase in self.test_case_dict.values():
            result += testcase.to_string()
        return result

    def set_cl_s(self, value: float):
        self.cl_s_redundancy = value

    def get_cl_s(self):
        return self.cl_s_redundancy

    def update_probe_dict(self):
        self.probe_dict = dict()    # probe cover info
        for test_case in self.test_case_dict.values():
            self.probe_dict.update(test_case.get_probe_dict())
        # self.probe_dict 清零
        for probe_id in self.probe_dict.keys():
            self.probe_dict[probe_id] = 0
        # self.probe_dict 累加
        for test_case in self.test_case_dict.values():
            for probe_id in test_case.get_probe_dict().keys():
                # 累计probe被多少条代码cover的次数
                # self.probe_dict[probe.get_name()] += probe.get_covered_times()
                # 累计probe被多少个testcase cover 的次数
                self.probe_dict[probe_id] += 1

    def get_probe_dict(self):
        return self.probe_dict

    def get_test_case_dict(self):
        return self.test_case_dict


def test_testclass():
    tc = TestClass()
    tc.parse_line("ACCURATE_PROBE probe_id_0")
    tc.parse_line("TESTCASE org.jfree.chart.annotations.junit.CategoryTextAnnotationTests.testHashcode")
    tc.parse_line("TESTCASE org.jfree.chart.annotations.junit.XYBoxAnnotationTests.testDrawWithNullInfo")
    tc.parse_line("ACCURATE_PROBE probe_id_0")
    tc.parse_line("ACCURATE_PROBE probe_id_1")
    tc.parse_line("ACCURATE_PROBE probe_id_2")
    tc.parse_line("ACCURATE_PROBE probe_id_2")
    tc.parse_line("TESTCASE org.jfree.chart.annotations.junit.CategoryTextAnnotationTests.testEquals")
    tc.parse_line("TESTCASE org.jfree.chart.annotations.junit.TextAnnotationTests.testHashCode")
    tc.parse_line("ACCURATE_PROBE probe_id_0")
    tc.parse_line("ACCURATE_PROBE probe_id_1")
    tc.parse_line("ACCURATE_PROBE probe_id_2")
    tc.update_probe_dict()
    print(tc.to_string())
    print(tc.get_probe_dict())


if __name__ == "__main__":
    test_testclass()
