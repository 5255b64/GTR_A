"""
构建TestSuite类
单个testsuite包含多个testclass的信息
"""
import os
import sys

from src.CONFIG import TESTCASE_STR_PREFIX, PROBE_COVER_PREFIX, PROBE_ID_PREFIX
from src.log_parser.test_class_parser import TestClass


class TestSuite:
    def __init__(self):
        """
        TestSuite类成员变量：
        test_suite_name:str
        test_class_dict:dict    该testsuite包含的所有testclass
                                字段类型
                                key为testclass的id
                                value为testclass对象
        test_class_ptr          当前parse到的test_class
        probe_dict:dict         当前testsuite的所有probe
                                key为probe_id
                                value=被cover的次数
        probe_inst_dict:dict    插入的所有桩 key=probe_id value=probe_type
        """
        self.test_suite_name = ""
        self.test_class_dict = dict()
        self.test_class_ptr = None
        self.probe_dict = dict()  # probe cover info
        self.probe_inst_dict = dict()

    def parse_line(self, line: str, isDebug: bool = False):
        tmp_list = line.replace(os.linesep, "").split(" ")
        if line.startswith(TESTCASE_STR_PREFIX):
            if len(tmp_list) is 2:
                # 发现testcase 判断是否是新的 testclass
                test_case_name = tmp_list[1]
                test_class_name = ".".join(test_case_name.split(".")[0:-1])
                if test_class_name not in self.test_class_dict.keys():
                    self.test_class_ptr = TestClass()
                    self.test_class_dict[test_class_name] = self.test_class_ptr
                else:
                    self.test_class_ptr = self.test_class_dict[test_class_name]
                self.test_class_ptr.parse_line(line, isDebug=isDebug)
            else:
                if isDebug:
                    print("TestSuite.parse_line:字符串格式有误-\"" + line + "\"", file=sys.stderr)
                return False
            return True
        elif line.startswith(PROBE_COVER_PREFIX):
            # 发现probe 调用TestClass.parse_line
            if self.test_class_ptr is not None and len(tmp_list) is 2:
                self.test_class_ptr.parse_line(line, isDebug=isDebug)
            else:
                if isDebug:
                    print("TestSuite.parse_line:testclass为None的情况下发现probe-\"" + line + "\"", file=sys.stderr)
                return False
            return True
        elif line.startswith(PROBE_ID_PREFIX):
            # 发现插桩信息 记录在self.probe_inst_dict
            if len(tmp_list) is 3:
                probe_id = tmp_list[1]
                probe_type = tmp_list[2]
                self.probe_inst_dict[probe_id] = probe_type
            else:
                if isDebug:
                    print("TestSuite.parse_line:字符串格式有误-\"" + line + "\"", file=sys.stderr)
                return False
            return True
        if isDebug:
            print("TestSuite.parse_line:未定义的前缀-\"" + line + "\"", file=sys.stderr)
        return False

    def set_name(self, name: str):
        self.test_suite_name = name

    def get_name(self):
        return self.test_suite_name

    def get_case_dict(self):
        return self.test_class_dict

    def to_string(self):
        result = ""
        for test_class_id in self.test_class_dict.keys():
            result += self.test_class_dict[test_class_id].to_string()
        return result

    def update_probe_dict(self):
        self.probe_dict = dict()  # probe cover info
        for test_class in self.test_class_dict.values():
            # 对test_class做一个update
            test_class.update_probe_dict()
            self.probe_dict.update(test_class.get_probe_dict())
        # self.probe_dict 清零
        for probe_id in self.probe_dict.keys():
            self.probe_dict[probe_id] = 0
        # self.probe_dict 累加
        for test_class in self.test_class_dict.values():
            class_probe_dict = test_class.get_probe_dict()
            for probe_id in class_probe_dict.keys():
                self.probe_dict[probe_id] += class_probe_dict[probe_id]

    def get_probe_dict(self):
        return self.probe_dict

    def get_probe_inst_dict(self):
        return self.probe_inst_dict

    def get_test_class_dict(self):
        return self.test_class_dict


def test_testsuite():
    ts = TestSuite()
    ts.parse_line("PROBE_ID probe_id_0 NORMAL")
    ts.parse_line("PROBE_ID probe_id_1 NORMAL")
    ts.parse_line("PROBE_ID probe_id_2 JUMP")
    ts.parse_line("PROBE_ID probe_id_3 JUMP")
    ts.parse_line("ACCURATE_PROBE probe_id_0")
    ts.parse_line("TESTCASE org.jfree.chart.annotations.junit.CategoryTextAnnotationTests.testHashcode")
    ts.parse_line("TESTCASE org.jfree.chart.annotations.junit.XYBoxAnnotationTests.testDrawWithNullInfo")
    ts.parse_line("ACCURATE_PROBE probe_id_0")
    ts.parse_line("ACCURATE_PROBE probe_id_1")
    ts.parse_line("ACCURATE_PROBE probe_id_2")
    ts.parse_line("ACCURATE_PROBE probe_id_2")
    ts.parse_line("TESTCASE org.jfree.chart.annotations.junit.CategoryTextAnnotationTests.testEquals")
    ts.parse_line("TESTCASE org.jfree.chart.annotations.junit.TextAnnotationTests.testHashCode")
    ts.parse_line("ACCURATE_PROBE probe_id_0")
    ts.parse_line("ACCURATE_PROBE probe_id_1")
    ts.parse_line("ACCURATE_PROBE probe_id_2")
    ts.update_probe_dict()
    print(ts.to_string())
    print(ts.get_probe_dict())
    print(ts.get_probe_inst_dict())


if __name__ == "__main__":
    test_testsuite()
