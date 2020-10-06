"""
保存所需的全局变量
"""
# TODO 修改所有
# 关键项
## 项目主文件夹位置
import os

MAIN_FOLDER = "/home/gx/Documents/TestMinimization/TestMinimization/py_classifier_2020"
## OUPUT文件位置
# RESULT_OUT_PATH = "/media/gx/0226E34626E338F5/GX/Study/ECNU/TestMinimization/py_classifier_2020/out_test"
RESULT_OUT_PATH = "/home/gx/Documents/TestMinimization/TestMinimization/py_classifier_2020/out"
# defects4j的主体程序
DEFECTS4J_PROJ_ADDR = "/home/gx/Documents/TestMinimization/defects4j-master"
# 临时文件夹 存储临时文件(需要时被创建 不需要时被删除)
TMP_ROOT_FOLDER = "/home/gx/Documents/TestMinimization/TestMinimization/py_classifier_2020/tmp"
# 存储被测项目源文件的目录
CHECKOUT_ROOT_FOLDER = "/home/gx/Documents/TestMinimization/TestMinimization/py_classifier_2020/checkout"
# debug文件存储位置
DEBUG_ROOT_FOLDER = "/home/gx/Documents/TestMinimization/TestMinimization/py_classifier_2020/debug"
## JVM
JVM = "java"
## python 解释器
PYTHON = "/home/gx/Documents/anaconda/envs/py36/bin/python"
## 多进程并行参数
NUM_PROCESS_ANALYSIS = 1  # analysis使用的线程数
NUM_PROCESS_ATTRITUBE_VERSION_LEVEL = 1  # attritube使用的线程数 version级别
NUM_PROCESS_ATTRITUBE_CASE_LEVEL = 1  # attritube使用的线程数 case级别

# lib文件夹位置
LIB_FOLDER_ARRD = MAIN_FOLDER + os.sep + "lib"

# defects4j相关文件目录（不包含defects4j的主体程序）
DEFECTS4J_FOLDER_ADDR = LIB_FOLDER_ARRD + os.sep + "defects4j"
# defects4j的环境变量 调用defects4j之前 一定要先调用该文件
DEFECTS4J_PRE_SOURCE_FILE_ADDR = DEFECTS4J_FOLDER_ADDR + os.sep + "AddPathDefects4j"
# defects4j的ant build文件模板
DEFECTS4J_ANT_BUILD_TEMPLATE_ADDR = DEFECTS4J_FOLDER_ADDR + os.sep + "defects4j.build.template.xml"
# DEFECTS4J_PRE_INCLUDE_FILE_ADDR = DEFECTS4J_FOLDER_ADDR + os.sep + "defects4j.include"
DEFECTS4J_PRE_INCLUDE_FILE_ADDR = DEFECTS4J_FOLDER_ADDR + os.sep + "defects4j_new.include"

# defects4j的主体程序
DEFECTS4J_PROJ_INFO_ADDR = DEFECTS4J_PROJ_ADDR + os.sep + "framework" + os.sep + "projects"
DEFECTS4J_PROJ_BUILD_FILE_ADDR = DEFECTS4J_PROJ_ADDR + os.sep + "framework" + os.sep + "projects" + os.sep + "defects4j.build.xml"

# jar包
JAR_ADDR = LIB_FOLDER_ARRD + os.sep + "jar"
JAR_CLASSPATH = "$CLASSPATH:" + JAR_ADDR + os.sep + "commons-cli-1.4.jar:" + JAR_ADDR + os.sep + "fastjson-1.2.62.jar:" + JAR_ADDR + os.sep + "tm.jar"
JAR_CLASS_ANT_BUILD_FILE_EDITOR = "sqslab.ecnu.edu.util.AntBuildFileEditor"
JAR_CLASS_JAVA_SOURCE_CODE_EDITOR = "sqslab.ecnu.edu.util.JavaSourceCodeEditor"
JAR_CLASS_JUNIT_LOG_EXTRACTOR = "sqslab.ecnu.edu.util.JunitLogExtractor"
JAR_CLASS_JUNIT_LOG_PARSER = "sqslab.ecnu.edu.util.JunitLogParser"
JAR_TEST_SUITE_FACTORY = "sqslab.ecnu.edu.util.TestSuiteFactory"

# bash脚本
BASH_FOLDER = LIB_FOLDER_ARRD + os.sep + "bash"
BASH_DEFECT4J = BASH_FOLDER + os.sep + "defects4j_interface.sh"
BASH_RUN_RANDOOP_WITH_DEFECTS4J = BASH_FOLDER + os.sep + "RunRandoopWithDefects4j.sh"
BASH_DEFECT4J_GEN_TESTCASE = BASH_FOLDER + os.sep + "Defects4jGenTestcase.sh"
BASH_DEFECT4J_CHECKOUT = BASH_FOLDER + os.sep + "Defects4jCheckout.sh"
BASH_DEFECT4J_GET_TEST_RESULT = BASH_FOLDER + os.sep + "Defects4jGetTestResult.sh"
BASH_RUN_MANNUAL_CASE_WITH_JAVAAGENT = BASH_FOLDER + os.sep + "RunMannualCaseWithJavaAgent.sh"
BASH_RUN_MANNUAL_CASE = BASH_FOLDER + os.sep + "RunMannualCase.sh"
BASH_RUN_MANNUAL_SINGLE_CASE_WITH_JAVAAGENT = BASH_FOLDER + os.sep + "RunMannualSingleCaseWithJavaAgent.sh"

# perl脚本
PERL_FOLDER = LIB_FOLDER_ARRD + '/perl'
PERL_RUN_TESTCASE_WITH_JAVA_AGENT = PERL_FOLDER + os.sep + "RunTestcasesWithJavaagent.pl"

# 项目相关信息
PROJ_LIST = ["Chart", "Closure", "Lang", "Math", "Mockito", "Time"]
PROJ_BUG_NUM_DICT = {"Chart": 26, "Closure": 176, "Lang": 65, "Math": 106, "Mockito": 38, "Time": 27}

PROJ_TEST_SOURCE_ADDR_LIST = [
    "src" + os.sep + "test" + os.sep + "java",
    "test",
    "tests",
]
PROJ_SOURCE_ADDR_LIST = [
    "src" + os.sep + "main" + os.sep + "java",
    "src",
    "source",
]
PROJ_CLASSES_ADDR_LIST = [
    "buildSrc" + os.sep + "build" + os.sep + "classes",
    "target" + os.sep + "classes",
    "build" + os.sep + "classes",
    "build",
]

## 每个项目的根包
PROJ_ROOT_PKG = {
    "Chart": "org.jfree.*",
    # "Closure": "com.google.javascript.*:com.google.debugging.*",
    "Closure": "com.google.*",
    "Lang": "org.apache.commons.lang*",
    "Math": "org.apache.commons.math*",
    "Mockito": "*",
    # "Mockito": "org.mockito*",
    "Time": "org.joda.time.*"}

# agent相关
# agent.jar文件位置
JAVAAGENT_JAR_ADDR = LIB_FOLDER_ARRD + os.sep + "jar" + os.sep + "agent.jar"
JACOCOCLI_JAR_ADDR = LIB_FOLDER_ARRD + os.sep + "jar" + os.sep + "jacococli.jar"
# agent参数前缀
JAVAAGENT_ARGS_PREFIX = "-javaagent:" + JAVAAGENT_JAR_ADDR
# JAVAAGENT_ARGS_PREFIX = "-Xshare:off -javaagent:" + JAVAAGENT_JAR_ADDR

# 聚类削减相关
## 聚类采样精度
CASE_PRECENT_FROM = 0  # 采样最小值
CASE_PRECENT_TO = 100  # 采样最大值
CASE_PRECENT_STEP = 5  # 采样步长
CASE_PRECENT_LIST = list(
    range(CASE_PRECENT_FROM + CASE_PRECENT_STEP, CASE_PRECENT_TO + CASE_PRECENT_STEP, CASE_PRECENT_STEP))
# CASE_PRECENT_LIST = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
# CASE_PRESENT_LIST = [90, 100]
CLUSTER_NUM_PRECENT = 10  # kmeans的聚类cluster数
RANDOM_REPEAT_TIMES = 2  # 包含随机因素的方法 进行多次计算取均值 的随机次数

# 脚本执行相关
SCRIPT_VERSION_TIMEOUT = 2000  # 单个version的执行timeout（秒） 超时则执行下一个version（当前version的线程无法停止）
RESULT_LOG_ADDR = RESULT_OUT_PATH + os.sep + "log"
RESULT_OUTPUT_ADDR = RESULT_OUT_PATH + os.sep + "result"
RESULT_OLD_OUTPUT_ADDR = RESULT_OUT_PATH + os.sep + "result_old"
RESULT_MIDDLE_DATA_ATTRIBUTE_PATH = RESULT_OUT_PATH + os.sep + "middle_data_attribute"
RESULT_MIDDLE_DATA_ANALYSIS_PATH = RESULT_OUT_PATH + os.sep + "middle_data_analysis"

# 添加bash所需环境变量
my_env = os.environ
# my_env["PERL_MB_OPT"] = "--install_base \"/home/gx/perl5\""
# my_env["PERL_MM_OPT"] = "/home/gx/perl5"
# my_env["INSTALL_BASE"] = "/home/gx/perl5"
# my_env["PERL_LOCAL_LIB_ROOT"] = "/home/gx/perl5:/home/gx/perl5"
# my_env["PERL5LIB"] = "/home/gx/perl5/lib/perl5:/home/gx/perl5/lib/perl5"
# my_env["PATH"] = "/home/gx/perl5/bin:/home/gx/perl5/bin:" + my_env["PATH"]

# IO 相关
JACOCO_RETRY_TIME_MAX: int = 1        # jacoco失败后 最多的重试次数
JACOCO_RETRY_TIME_DELAY = 0.001     # jacoco生成失败后 延时时间
