"""
构建Probe类
收集单个probe的信息
"""
import os
import sys

from src.CONFIG import PROBE_COVER_PREFIX


class Probe:
    def __init__(self):
        """
        Probe类成员变量：
        probe_name              桩标识
        # probe_type              桩类型(NORMAL/JUMP）
        probe_covered_times     桩被覆盖的次数
        """
        self.probe_name = ""  # 桩标识
        # self.probe_type = ""  # 桩类型
        self.probe_covered_times = 0

    def parse(self, probe_str: str, isDebug:bool=False):
        """
        ”PROBE_ID“为probe的前缀标识
        :param probe_str:   桩表示字符串 格式为
                            “PROBE_ID {probe_name} {probe_type}”
                            例：“PROBE_ID probe_id_0 JUMP”
        :return:
        """
        tmp_list = probe_str.replace(os.linesep, "").split(" ")
        if len(tmp_list) is 2 and tmp_list[0] == PROBE_COVER_PREFIX:
            self.probe_name = tmp_list[1]
            return True
        else:
            if isDebug:
                print("Probe.parse:字符串格式有误-\"" + probe_str + "\"", file=sys.stderr)
            return False

    def to_string(self):
        return self.probe_name + "\t" + str(self.probe_covered_times)

    def get_name(self):
        return self.probe_name

    # def get_type(self):
    #     return self.probe_type

    def get_covered_times(self):
        return self.probe_covered_times

    def cover_one_more_time(self):
        self.probe_covered_times += 1


def test_probe():
    probe_str = "ACCURATE_PROBE probe_id_0"
    probe = Probe()
    probe.parse(probe_str)
    print(probe.to_string())


if __name__ == "__main__":
    test_probe()
