# TODO 重构

from src.utils import sub_call_hook
from src.CONFIG import JAR_CLASSPATH, JAR_CLASS_JUNIT_LOG_PARSER, JVM


def run(inputFileAddr: str, outputFileAddr: str):
    """
    interface for sqslab.ecnu.edu.util.JunitLogExtractor
    :param inputFileAddr:
    :param outputFileAddr:
    :return:
    """
    cmd = [
        JVM, "-cp", JAR_CLASSPATH, JAR_CLASS_JUNIT_LOG_PARSER,
        "-i", inputFileAddr,
        "-o", outputFileAddr
    ]
    # print(" ".join(cmd))
    sub_call_hook.serial(cmd)


if __name__ == "__main__":
    # run(
    #     inputFileAddr="../../../tmp_not_delete/junit.extracted.log",
    #     outputFileAddr="../../../tmp_not_delete/junit.parsed.attr.json")
    run(
        inputFileAddr="/media/gx/0226E34626E338F5/GX/Study/ECNU/TestMinimization/py_classifier_2020/tmp/Lang/randoop/1/junit.log",
        outputFileAddr="/media/gx/0226E34626E338F5/GX/Study/ECNU/TestMinimization/py_classifier_2020/tmp/Lang/randoop/1/attr.json")
