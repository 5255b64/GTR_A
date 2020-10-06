"""
调用系统shell命令

对subprocess做hook操作
控制stdout、stderr的输出
相当于日志控制
"""
import os
import subprocess

from src.CONFIG import my_env


def serial(cmd):
    """
    对subprocess.call做hook
    该方法必须等到获得调用返回至之后 再执行下一步语句
    是串行的
    :param cmd:
    :return:
    """
    with open(os.devnull, 'w') as devnull:
        subprocess.call(
            cmd,
            # stdout=devnull,
            # stderr=devnull,
            env=my_env,
            # shell=True
        )


def serial_all(cmd):
    subprocess.call(
        cmd,
        env=os.environ,
        # shell=True

    )


def serial_stderr(cmd):
    with open(os.devnull, 'w') as devnull:
        subprocess.call(
            cmd,
            stdout=devnull,
            env=os.environ,
            # shell=True
        )


def serial_none(cmd):
    with open(os.devnull, 'w') as devnull:
        subprocess.call(
            cmd,
            stdout=devnull,
            stderr=devnull,
            env=my_env,
            # shell=True
        )


if __name__ == "__main__":
    # serial_all(["/home/gx/Software/anaconda3/envs/py36/bin/python",
    #             "/media/gx/0226E34626E338F5/GX/Study/ECNU/TestMinimization/py_classifier_2020/src/script/script_get_result_data.py"])
    # with open("/home/gx/Desktop/text.txt", 'a') as f:
    serial([])
