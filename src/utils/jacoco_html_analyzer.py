# TODO 重构
from abc import ABC
from html.parser import HTMLParser
from html.entities import name2codepoint

from src.utils import file_helper
from src.utils.file_helper import getallfile
from src.utils import logger


class MyHTMLParser(HTMLParser):
    def __init__(self, out_file_addr: str, java_class_name: str):
        super(MyHTMLParser, self).__init__()
        self.__out_file_addr = out_file_addr
        self.__java_class_name = java_class_name

        self.__counter = 0

    def print_counter(self):
        print(self.__counter)

    def handle_starttag(self, tag, attrs):
        # print("Start tag:", tag)
        # for x in range(len(attrs)):
        #     for y in range(len(attrs[x])):
        #         print(attrs[x][y], end=" ")

        if len(attrs) is 2:
            if attrs[0][0] == "class" and (
                    attrs[0][1] == "fc"
                    or attrs[0][1] == "fc bfc"
                    or attrs[0][1] == "pc"
                    or attrs[0][1] == "pc bpc"
                    # attrs[0][1] == "nfc"
                    # attrs[0][1] == "nfc bnc"
            ):
                self.__counter += 1
                # print(attrs[0][0] + "=" + attrs[0][1] + " " + attrs[1][0] + "=" + attrs[1][1])
                with open(self.__out_file_addr, "a") as f_out:
                    f_out.write(self.__java_class_name + " " + attrs[1][1] + "\n")
        # for attr in attrs:
        #     for x in attr:
        #         print(x+":"+attrs[x])

    def handle_endtag(self, tag):
        pass
        # print("End tag  :", tag)

    def handle_data(self, data):
        pass
        # print("Data     :", data)

    def handle_comment(self, data):
        pass
        # print("Comment  :", data)

    def handle_entityref(self, name):
        pass
        # c = chr(name2codepoint[name])
        # print("Named ent:", c)

    def handle_charref(self, name):
        pass
        # if name.startswith('x'):
        #     c = chr(int(name[1:], 16))
        # else:
        #     c = chr(int(name))
        # print("Num ent  :", c)

    def handle_decl(self, data):
        pass
        # print("Decl     :", data)

    def set_java_class_name(self, java_class_name):
        self.__java_class_name = java_class_name


def run(html_path: str, output_addr: str):
    all_files = getallfile(html_path)
    if len(all_files) is 0:
        # logger.err("未能生成jacoco数据：\t" + html_path)
        return

    file_helper.check_file_exists(output_addr)

    # 生成输出文件 避免没有输出的情况下不产生文件
    with open(output_addr, "w") as f:
        f.write("")

    parser = MyHTMLParser(output_addr, "none")
    for abs_file_attr in all_files:
        if abs_file_attr.endswith(".html"):
            # print("FILE:\t"+abs_file_attr)
            parser.reset()
            with open(abs_file_attr, "r") as f_in:
                for line in f_in.readlines():
                    temp = abs_file_attr.split("/")
                    parser.set_java_class_name(temp[-2] + "." + temp[-1].replace(".html", "").replace(".java", ""))
                    parser.feed(line)
    # TODO
    #  不使用parser.close()是否会残留内存
    #  使用parser.close()是否会在数据未处理完之前结束
    parser.close()
    # parser.print_counter()
    return True


if __name__ == "__main__":
    run(
        html_path="/tmp/tmp_root_folder/Lang/tmp_Lang_1/tmp_step2/jacoco_output",
        output_addr="/tmp/123/xxx"
    )
    print("hello world")
