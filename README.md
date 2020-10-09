# GTR-A：Generated Testcase Redundancy Analysis
## 简介
本项目针对Java自动化测试用例生成方法中，可能存在的测试冗余问题，进行分析、探究。
实验对象采用了Defects4j中提供的Java项目。
## 目录结构
1. GTR_A
    - -lib *外部依赖*
        - +bash *bash脚本*
        - +defects4j_cfg *defects4j相关的配置文件*
        - +jar *使用到的jar包 主要是jacoco日志插桩程序以及日志分析程序*
        - +defects4j_proj *defects4j项目主目录*
    - +out *保存输出文件*
    - +tmp *保存临时文件*
    - -src *python源代码*
        - +defects4j_setup *对defects4j项目进行初始化*
        - +defects4j_test_generator *用于生成测试用例*
        - +defects4j_test_mutator *用于执行变异测试*
        - +defects4j_test_runner *用于执行测试用例*
        - +interface *用于执行lib中的外部程序*
            - +java
            - +bash
        - +utils *通用软件工具*
        - +main *主要的执行脚本*
        - CONFIG.py *配置文件 存储常量*
    - README.md *项目说明文当*
    
2. -out *保存输出文件*
    - -testsuite *保存生成的测试用例*
        - -mannual
        - -randoop
        - -evosuite
    - -log *保存执行之后生成的日志*
        - -mannual
        - -randoop
        - -evosuite
    - -mutation *保存变异测试数据*
        - -mannual
        - -randoop
        - -evosuite
    
3. -tmp *保存临时文件*
    - checkout *保存SUT的项目文件*
    - log *保存中间日志文件（比如antlog）*
    - test *保存debug过程中生成的文件*
## 注意事项
1. “out”文件夹与“tmp”文件夹可以重定向。
2. 在defects4j的fixed与buggy版本中，只考虑buggy版本(*b)。

## TodoList
- [ ] Setup
    - [x] 修改CONFIG.py配置文件
    - [x] 修改所有的interface
    - [x] 修改所有的utils
- [ ] 生成测试用例
    - [x] 人工测试用例
    - [x] randoop与evosuite
- [ ] 修改jacoco
    - [x] 区分NORMAL桩和JUMP桩
- [ ] 执行测试用例
    - [x] 修改build文件 插桩
    - [x] 执行用例 获取数据
      - [ ] 编写进程池
- [x] 执行变异测试
- [ ] 编写执行脚本
    - [ ] 执行所有version 获取日志信息
- [ ] 日志分析
    - [ ] 编写testcase类
      - [ ] 桩信息
        - [ ] 桩类别（NORMAL、JUMP）
    - [ ] 编写testclass类
      - [ ] 包含的testcase列表
    - [ ] 编写testsuite类
      - [ ] 包含的testclass列表
      - [ ] 变异测试结果
    - [ ] 对象序列化
      - [ ] 避免重复计算


​    
