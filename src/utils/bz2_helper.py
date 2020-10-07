"""
用于压缩、解压文件
"""
import os
import tarfile

from utils import file_helper


def compress(input_addr: str, output_bz2_file_name: str):
    # cmd = ["tar", "-cjf", bz2_file_abs_name, input_testsuite_addr + "/*"]
    # sub_call_hook.serial(" ".join(cmd))
    cur_path = os.getcwd()
    os.chdir(input_addr)
    tar = tarfile.open(output_bz2_file_name, "w:bz2")
    for file in os.listdir(input_addr):
        # fullpath = input_testsuite_addr+"/"+file
        tar.add(file)
    tar.close()
    os.chdir(cur_path)


def unzip(output_addr: str, intput_bz2_file_name: str):
    tar = tarfile.open(intput_bz2_file_name)
    names = tar.getnames()
    file_helper.check_path_exists(output_addr)
    for name in names:
        tar.extract(name, output_addr)
    tar.close()


def test_compress():
    input_addr = "/home/gx/Documents/TestMinimization/GTR_A/tmp/test/Lang/1b/evosuite/org"
    output_bz2_file_name = "/home/gx/Documents/TestMinimization/GTR_A/tmp/test/Lang/1b/evosuite/xxx.tar.bz2"
    compress(input_addr=input_addr, output_bz2_file_name=output_bz2_file_name)


def test_unzip():
    output_addr = "/home/gx/Documents/TestMinimization/GTR_A/tmp/test/Lang/1b/evosuite/xxx"
    intput_bz2_file_name = "/home/gx/Documents/TestMinimization/GTR_A/tmp/test/Lang/1b/evosuite/1b.tar.bz2"
    unzip(output_addr, intput_bz2_file_name)


if __name__ == "__main__":
    test_compress()
    # test_unzip()
