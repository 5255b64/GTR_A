# TODO 重构

from src.utils import sub_call_hook
from src.CONFIG import JAR_CLASSPATH, JAR_CLASS_ANT_BUILD_FILE_EDITOR, \
    DEFECTS4J_ANT_BUILD_TEMPLATE_ADDR, JVM


def run(inputFileAddr: str, outputFileAddr: str, javaagentArgs: str, outputErrPath: str, outputAlltestPath: str):
    """
    interface for sqslab.ecnu.edu.util.AntBuildFileEditor
    :param outputAlltestPath:
    :param inputFileAddr:
    :param outputFileAddr:
    :param javaagentArgs:
    :param outputErrPath:
    :return:
    """
    cmd = [
        JVM, "-cp", JAR_CLASSPATH, JAR_CLASS_ANT_BUILD_FILE_EDITOR,
        "-i", inputFileAddr,
        "-o", outputFileAddr,
        "-a", javaagentArgs,
        "-e", outputErrPath,
        "-t", outputAlltestPath
    ]
    # print(" ".join(cmd))
    sub_call_hook.serial(cmd)


if __name__ == "__main__":
    run(
        inputFileAddr=DEFECTS4J_ANT_BUILD_TEMPLATE_ADDR,
        outputFileAddr="/media/gx/0226E34626E338F5/GX/Study/ECNU/TestMinimization/py_classifier_2020/tmp_not_delete/defects4j.build.xml",
        javaagentArgs="hahaha",
        outputErrPath="err",
        outputAlltestPath="alltest")
