# TODO 重构

from src.utils import sub_call_hook
from src.CONFIG import JAR_CLASSPATH, JAR_TEST_SUITE_FACTORY, JVM


def run(json_input: str, testsuite_addr_input: str, output_addr: str):
    """
    interface for sqslab.ecnu.edu.util.JunitLogExtractor
    :param json_input:
    :param testsuite_addr_input:
    :param output_addr:
    :return:
    """

    cmd = [
        JVM, "-cp", JAR_CLASSPATH, JAR_TEST_SUITE_FACTORY,
        "-j", json_input,
        "-t", testsuite_addr_input,
        "-o", output_addr
    ]
    # print(" ".join(cmd))
    sub_call_hook.serial(cmd)


if __name__ == "__main__":
    run(
        json_input="/media/gx/0226E34626E338F5/GX/Study/ECNU/TestMinimization/py_classifier_2020/tmp_not_delete/testsuite_edit_test/minimization.json",
        testsuite_addr_input="/media/gx/0226E34626E338F5/GX/Study/ECNU/TestMinimization/py_classifier_2020/tmp_not_delete/testsuite_edit_test/before",
        output_addr="/media/gx/0226E34626E338F5/GX/Study/ECNU/TestMinimization/py_classifier_2020/tmp_not_delete/testsuite_edit_test/after"
    )
