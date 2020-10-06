# TODO 重构

from src.utils import sub_call_hook
from src.CONFIG import JAR_CLASSPATH, JAR_CLASS_JUNIT_LOG_EXTRACTOR, JVM


def run(inputFileAddr: str, outputFileAddr: str):
    """
    interface for sqslab.ecnu.edu.util.JunitLogExtractor
    :param inputFileAddr:
    :param outputFileAddr:
    :return:
    """
    cmd = [
        JVM, "-cp", JAR_CLASSPATH, JAR_CLASS_JUNIT_LOG_EXTRACTOR,
        "-i", inputFileAddr,
        "-o", outputFileAddr
    ]
    # print(" ".join(cmd))
    sub_call_hook.serial(cmd)


if __name__ == "__main__":
    # sub_call_hook.serial(["tail", "../../../tmp_not_delete/junit.template.log"])
    run(
        inputFileAddr="../../../tmp_not_delete/junit.template.log",
        outputFileAddr="../../../tmp_not_delete/junit.extracted.log")
