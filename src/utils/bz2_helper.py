"""
用于压缩、解压文件
"""
import os
import tarfile


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
