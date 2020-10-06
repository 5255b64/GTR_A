# TODO 重构

from src.utils import sub_call_hook
from src.CONFIG import JAR_CLASSPATH, JAR_CLASS_JAVA_SOURCE_CODE_EDITOR, JVM


def run(inputFileAddr: str, outputFileAddr: str):
    """
    interface for sqslab.ecnu.edu.util.JavaSourceCodeEditor
    :param inputFileAddr:
    :param outputFileAddr:
    :return:
    """
    cmd = [
        JVM, "-cp", JAR_CLASSPATH, JAR_CLASS_JAVA_SOURCE_CODE_EDITOR,
        "-i", inputFileAddr,
        "-o", outputFileAddr
    ]
    # print(" ".join(cmd))
    sub_call_hook.serial(cmd)


if __name__ == "__main__":
    # run(
    #     inputFileAddr="../../../tmp_not_delete/testcase_template_not_modified.java",
    #     outputFileAddr="../../../tmp_not_delete/testcase_template_modified.java")
    run(
        inputFileAddr="/tmp/py_classifier_2020/AnnotationUtilsTest.java",
        outputFileAddr="/tmp/py_classifier_2020/AnnotationUtilsTest2.java")
