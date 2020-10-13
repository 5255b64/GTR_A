"""
分析单个junit日志
每一个日志文件代表一个testsuite
"""
from src.log_parser.test_suite_parser import TestSuite


# TODO 分析数据
class LogParser:
    def __init__(self):
        """
        LogParser类成员变量：
        test_suite      当前log文件对应的test_suite对象
        """
        self.test_suite = TestSuite()

    def parse_file(self, file: str):
        """
        分析log文件
        调用parse_line分析每一行
        TODO 计算每个testcase的冗余指标
        TODO 计算整个testsuite的冗余指标
        :param file:
        :return:
        """
        with open(file, 'r') as f:
            line = f.readline()
            while line:
                self.parse_line(line)
                line = f.readline()

    def parse_line(self, line: str):
        """
        从日志信息中分析其中一行
        :param line:
        :return:
        """
        self.test_suite.parse_line(line)

    def update_probe_dict(self):
        self.test_suite.update_probe_dict()

    def to_string(self):
        return self.test_suite.to_string()

    def get_test_suite(self):
        return self.test_suite


def test_log_parser():
    file_addr = "/run/media/gx/仓库/GTR_A/out/log/manual/Chart/2.log"
    log_parser = LogParser()
    log_parser.parse_file(file_addr)
    print(log_parser.to_string())


if __name__ == "__main__":
    test_log_parser()
