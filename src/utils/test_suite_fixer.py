"""
编辑.java测试用例文件
在每一个单元测试方法开始时
输出方法名

对被修改的文件进行备份(.bkb)
直接在源文件上修改

根据方法名的前缀和关键字来判断哪个方法是testcase
public void testXXXX()

"""
import os

from utils import file_helper
import re

pattern_func = r'public +void +test[\w]+ *\( *\)'
pattern_package = r'package [\w.]+;'
pattern_import = r'import [\w.]+;'
pattern_pkg = re.compile(pattern_package)
pattern_func = re.compile(pattern_func)
pattern_import = re.compile(pattern_import)


def fun(input_file_addr: str, output_file_addr: str):
    file_helper.cp(input_file_addr, output_file_addr)
    with open(input_file_addr, 'r') as f_before:
        with open(output_file_addr, 'w') as f_after:
            package_name = ""
            class_name = ""
            line = f_before.readline()
            # 寻找package
            flag = True
            while line and flag:
                result_pkg = pattern_pkg.search(line)
                result_import = pattern_import.search(line)
                if result_pkg is not None:
                    package_name = line.replace("package", "").replace(" ", "").replace(";", "").replace(
                        os.linesep, "")
                    # print(package_name)
                    flag = False
                elif result_import is not None:
                    # print(line)
                    flag = False
                # print(line, end="")
                f_after.write(line)

                line = f_before.readline()
            # 寻找 class name 根据.java文件名生成
            class_name = input_file_addr.split(os.sep)[-1].replace(".java", "").replace(".bkb", "")
            # 搜索每一个以public void test开头的function
            pattern = re.compile(pattern_func)
            flag = False
            method_name = "-1"
            while line:
                if not flag:
                    result = pattern.search(line)
                    if result is not None:
                        lines = line.split(" ")
                        for temp in lines:
                            if temp.startswith("test"):
                                method_name = temp.replace(os.linesep, "").replace("{", "").replace("(", "").replace(
                                    ")", "")
                                break
                        flag = True
                        if "{" in line:
                            flag = False
                            lines = line.split("{", 2)
                            print_msg = get_print_msg(package_name, class_name, method_name)
                            new_line = lines[0] + "{" + "System.out.println(\"TESTCASE " + print_msg + "\");" + lines[1]
                            # print(new_line, end="")
                            f_after.write(new_line)
                        else:
                            f_after.write(line)
                    else:
                        # print(line, end="")
                        f_after.write(line)
                else:
                    if "{" in line:
                        flag = False
                        lines = line.split("{", 2)
                        print_msg = get_print_msg(package_name, class_name, method_name)
                        new_line = lines[0] + "{" + "System.out.println(\"TESTCASE " + print_msg + "\");" + lines[1]
                        # print(new_line, end="")
                        f_after.write(new_line)
                    else:
                        # print(line, end="")
                        f_after.write(line)
                line = f_before.readline()


def get_print_msg(package_name: str, class_name: str, method_name: str):
    print_msg = ""
    if package_name != "":
        print_msg = package_name
    if class_name != "":
        if print_msg != "":
            print_msg += "." + class_name
        else:
            print_msg = class_name
    print_msg += "." + method_name
    return print_msg


if __name__ == "__main__":
    output_addr = "/run/media/gx/仓库/GTR_A/out/testsuite/randoop/Chart/1/tmp_testsuite/RegressionTest0.java"
    input_addr = output_addr + ".bkb"
    fun(input_addr, output_addr)
