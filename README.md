# GTR-A：Generated Testcase Redundancy Analysis
## 简介
本项目针对Java自动化测试用例生成方法中，可能存在的测试冗余问题，进行分析、探究。
实验对象采用了Defects4j中提供的Java项目。
## 目录结构
- GTR_A
    - -lib *外部依赖*
        - +bash *bash脚本*
        - +defects4j_cfg *defects4j相关的配置文件*
        - +jar *使用到的jar包 主要是jacoco日志插桩程序以及日志分析程序*
        - +perl *perl脚本*
        - +defects4j_proj *defects4j项目主目录*
    - -out *保存输出文件*
        - -testsuite *保存生成的测试用例*
            - -mannual
            - -randoop
            - -evosuite
        - -log *保存执行之后生成的日志*
            - -mannual
            - -randoop
            - -evosuite
    - -tmp *保存临时文件*
        - checkout *保存SUT的项目文件*
        - log *保存中间日志文件（比如antlog）*
    - -src *python源代码*
        - +defects4j_setup *对defects4j项目进行初始化*
        - +defects4j_test_generator *用于生成测试用例*
        - +defects4j_test_mutator *用于执行变异测试*
        - +defects4j_test_runner *用于执行测试用例*
        - +interface *用于执行lib中的外部程序*
            - +java
            - +bash
            - +perl
        - +utils *通用软件工具*
        - +main *主要的执行脚本*
        - CONFIG.py *配置文件 存储常量*
    - README.md *项目说明文当*
    
