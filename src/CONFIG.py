# TODO 修改所有
"""
保存所需的全局变量
"""
import os

# 项目目录相关
# # 主目录
MAIN_FOLDER = "/home/gx/Documents/TestMinimization/GTR_A"
# # tmp目录 存储临时文件(需要时被创建 不需要时清空)
TMP_FOLDER = MAIN_FOLDER + "/tmp"
# # out目录
OUT_FOLDER = MAIN_FOLDER + "/out"

# # 主目录之下
# # # tmp/lib目录
LIB_FOLDER = MAIN_FOLDER + os.sep + "lib"

# # # # tmp/lib/defects4j_proj defects4j的主体程序
DEFECTS4J_PROJ_ADDR = LIB_FOLDER + os.sep + "defects4j_proj"
# # # # # defects4j的主体程序
DEFECTS4J_PROJ_INFO_ADDR = DEFECTS4J_PROJ_ADDR + os.sep + "framework" + os.sep + "projects"
# # # # # defects4j的build文件
DEFECTS4J_PROJ_BUILD_FILE_ADDR = DEFECTS4J_PROJ_ADDR + os.sep + "framework" + os.sep + "projects" + os.sep + "defects4j.build.xml"

# # # # tmp/lib/defects4j_cfg defects4j配置文件目录
DEFECTS4J_CFG_FOLDER = LIB_FOLDER + os.sep + "defects4j_cfg"
# # # # # defects4j的环境变量 调用defects4j之前 一定要先调用该文件
DEFECTS4J_ADD_PATH_FILE = DEFECTS4J_CFG_FOLDER + os.sep + "AddPathDefects4j"
# # # # # defects4j的build文件模板
DEFECTS4J_ANT_BUILD_TEMPLATE_ADDR = DEFECTS4J_CFG_FOLDER + os.sep + "defects4j.build.template.xml"
# # # # # defects4j的include文件模板
DEFECTS4J_PRE_INCLUDE_FILE_ADDR = DEFECTS4J_CFG_FOLDER + os.sep + "defects4j_new.include"

# # # # lib/jar目录 保存jar包
JAR_FOLDER = LIB_FOLDER + os.sep + "jar"
# # # # lib/bash目录 保存bash脚本
BASH_FOLDER = LIB_FOLDER + os.sep + "bash"
# # # # lib/perl目录 保存perl脚本
PERL_FOLDER = LIB_FOLDER + '/perl'

# # tmp目录之下
# # # tmp/checkout目录 存储被测项目源文件的目录
CHECKOUT_FOLDER = TMP_FOLDER + "/checkout"
# # # tmp/log目录 存储debug生成的文件
TMP_LOG_FOLDER = TMP_FOLDER + "/log"
# # # tmp/test目录 存储debug生成的文件
TMP_TEST_FOLDER = TMP_FOLDER + "/test"
# debug文件存储位置
# DEBUG_ROOT_FOLDER = "/home/gx/Documents/TestMinimization/TestMinimization/py_classifier_2020/debug"

# # out目录之下
# # # out/log 输出日志目录
OUT_LOG_FOLDER = OUT_FOLDER + os.sep + "log"
# # # out/testsuite 测试用例目录
OUT_LOG_TESTSUITE = OUT_FOLDER + os.sep + "testsuite"

# 外部依赖相关
# # JVM java解释器
JVM = "/usr/bin/jvm/jdk1.8.0_261/bin/java"
# # python 解释器
PYTHON = "/home/gx/Documents/anaconda/envs/py36/bin/python"

# jar包
# # java的classpath
JAR_COMMONS_CLI = JAR_FOLDER + os.sep + "commons-cli-1.4.jar"
JAR_FASTJSON = JAR_FOLDER + os.sep + "fastjson-1.2.62.jar"
JAR_TM = JAR_FOLDER + os.sep + "tm.jar"
JAR_CLASSPATH = "$CLASSPATH:" + JAR_COMMONS_CLI + ":" + JAR_FASTJSON + ":" + JAR_TM
# JAR_CLASSPATH = "$CLASSPATH:" + JAR_FOLDER + os.sep + "commons-cli-1.4.jar:" + JAR_FOLDER + os.sep + "fastjson-1.2.62.jar:" + JAR_FOLDER + os.sep + "tm.jar"
# # 一些jar包中的class的直接目录
JAR_CLASS_ANT_BUILD_FILE_EDITOR = "sqslab.ecnu.edu.util.AntBuildFileEditor"
JAR_CLASS_JAVA_SOURCE_CODE_EDITOR = "sqslab.ecnu.edu.util.JavaSourceCodeEditor"
JAR_CLASS_JUNIT_LOG_EXTRACTOR = "sqslab.ecnu.edu.util.JunitLogExtractor"
JAR_CLASS_JUNIT_LOG_PARSER = "sqslab.ecnu.edu.util.JunitLogParser"
JAR_TEST_SUITE_FACTORY = "sqslab.ecnu.edu.util.TestSuiteFactory"

# bash脚本
BASH_DEFECT4J = BASH_FOLDER + os.sep + "defects4j_interface.sh"
BASH_RUN_RANDOOP_WITH_DEFECTS4J = BASH_FOLDER + os.sep + "RunRandoopWithDefects4j.sh"
BASH_DEFECT4J_GEN_TESTCASE = BASH_FOLDER + os.sep + "Defects4jGenTestcase.sh"
BASH_DEFECT4J_RUN_TEST_WITH_AGENT = BASH_FOLDER + os.sep + "Defects4jRunTestWithAgent.sh"
BASH_DEFECT4J_CHECKOUT = BASH_FOLDER + os.sep + "Defects4jCheckout.sh"
BASH_DEFECT4J_GET_TEST_RESULT = BASH_FOLDER + os.sep + "Defects4jGetTestResult.sh"
BASH_RUN_MANNUAL_CASE_WITH_JAVAAGENT = BASH_FOLDER + os.sep + "RunMannualCaseWithJavaAgent.sh"
BASH_RUN_MANNUAL_CASE = BASH_FOLDER + os.sep + "RunMannualCase.sh"
BASH_RUN_MANNUAL_SINGLE_CASE_WITH_JAVAAGENT = BASH_FOLDER + os.sep + "RunMannualSingleCaseWithJavaAgent.sh"

# 项目相关信息
# # 项目名称list
PROJ_LIST = ["Chart", "Cli", "Closure", "Codec", "Collections", "Compress", "Csv",
             "Gson", "JacksonCore", "JacksonDatabind", "JacksonXml", "Jsoup", "JxPath",
             "Lang", "Math", "Mockito", "Time"]
# # 每个项目的版本数
PROJ_VERSION_NUM = {
    "Chart": 26,
    "Cli": 40,
    "Closure": 176,
    "Codec": 18,
    "Collections": 28,
    "Compress": 47,
    "Csv": 16,
    "Gson": 18,
    "JacksonCore": 26,
    "JacksonDatabind": 112,
    "JacksonXml": 6,
    "Jsoup": 93,
    "JxPath": 22,
    "Lang": 65,
    "Math": 106,
    "Mockito": 38,
    "Time": 27
}
# # TODO 每个项目的test代码文件根目录
PROJ_TEST_SOURCE_ADDR_LIST = [
    "src" + os.sep + "test" + os.sep + "java",
    "src" + os.sep + "test",
    "test",
    "tests",
    "gson" + os.sep + "src" + os.sep + "test" + os.sep + "java",
]
# # TODO 每个项目的src代码文件根目录
PROJ_SOURCE_ADDR_LIST = [
    "src" + os.sep + "main" + os.sep + "java",
    "src",
    "source",
]
# # TODO 每个项目的class文件根目录
PROJ_CLASSES_ADDR_LIST = [
    "buildSrc" + os.sep + "build" + os.sep + "classes",
    "target" + os.sep + "classes",
    "build" + os.sep + "classes",
    "build",
]

# # TODO 每个项目的根包
PROJ_ROOT_PKG = {
    "Chart": "org.jfree.*",
    # "Closure": "com.google.javascript.*:com.google.debugging.*",
    "Closure": "com.google.*",
    "Lang": "org.apache.commons.lang*",
    "Math": "org.apache.commons.math*",
    "Mockito": "*",
    # "Mockito": "org.mockito*",
    "Time": "org.joda.time.*"
}

# agent相关
# # agent.jar文件位置
JAVAAGENT_JAR_ADDR = JAR_FOLDER + os.sep + "jacoco.jar"
# JAVAAGENT_JAR_ADDR = JAR_FOLDER + os.sep + "jacoco_blank.jar"
JACOCOCLI_JAR_ADDR = JAR_FOLDER + os.sep + "jacococli.jar"

# # agent参数前缀
JAVAAGENT_ARGS_PREFIX = "-javaagent:" + JAVAAGENT_JAR_ADDR
# JAVAAGENT_ARGS_PREFIX = "-Xshare:off -javaagent:" + JAVAAGENT_JAR_ADDR

# 脚本执行相关
SCRIPT_VERSION_TIMEOUT = 2000  # 单个version的执行timeout（秒） 超时则执行下一个version（当前version的线程无法停止）
# RESULT_OUTPUT_ADDR = OUT_FOLDER + os.sep + "result"
# RESULT_OLD_OUTPUT_ADDR = OUT_FOLDER + os.sep + "result_old"
# RESULT_MIDDLE_DATA_ATTRIBUTE_PATH = OUT_FOLDER + os.sep + "middle_data_attribute"
# RESULT_MIDDLE_DATA_ANALYSIS_PATH = OUT_FOLDER + os.sep + "middle_data_analysis"

# 添加bash所需环境变量
my_env = os.environ
# my_env["PERL_MB_OPT"] = "--install_base \"/home/gx/perl5\""
# my_env["PERL_MM_OPT"] = "/home/gx/perl5"
# my_env["INSTALL_BASE"] = "/home/gx/perl5"
# my_env["PERL_LOCAL_LIB_ROOT"] = "/home/gx/perl5:/home/gx/perl5"
# my_env["PERL5LIB"] = "/home/gx/perl5/lib/perl5:/home/gx/perl5/lib/perl5"
# my_env["PATH"] = "/home/gx/perl5/bin:/home/gx/perl5/bin:" + my_env["PATH"]

# IO 相关
JACOCO_RETRY_TIME_MAX: int = 1  # jacoco失败后 最多的重试次数
JACOCO_RETRY_TIME_DELAY = 0.001  # jacoco生成失败后 延时时间
