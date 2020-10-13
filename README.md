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
        - -manual
        - -randoop
        - -evosuite
    - -log *保存执行之后生成的日志*
        - -manual
        - -randoop
        - -evosuite
    - -mutation *保存变异测试数据*
        - -manual
        - -randoop
        - -evosuite
    
3. -tmp *保存临时文件*
    - checkout *保存SUT的项目文件*
    - log *保存中间日志文件（比如antlog）*
    - test *保存debug过程中生成的文件*
## 注意事项
1. “out”文件夹与“tmp”文件夹可以重定向。
2. 在defects4j的fixed与buggy版本中，只考虑buggy版本(*b)。

## 冗余指标

1. 基本冗余指标（父子集合冗余指标），子集合Cs与父集合Cf，先用父集合Cf减去子集合Cs，然后查看减去时候，Cs覆盖的某个probe p在父集合Cf中的数量是否仍大于0；若是，则Cs相对与Cf来说，关于p是冗余的；统计所有的probe的冗余情况，以冗余probe的数量百分比，作为基本冗余指标；
   1. 测试用例testcase相对于测试类testclass的冗余(CaCl冗余)；
   2. 测试用例testcase相对于测试套件testsuite的冗余(CaS冗余)；
   3. 测试类testclass相对于测试套件testsuite的冗余(ClS冗余)；
2. 细化冗余指标 考虑到基本冗余指标对于较大的父集合，会大概率将子集合判断为高冗余；因此，要对冗余指标进行细化，不只考虑probe是否被覆盖，还要计算probe被覆盖的次数；probe覆盖次数越高，冗余指标应该越大；

## TodoList
### Setup
- [x] 修改CONFIG.py配置文件
- [x] 修改所有的interface
- [x] 修改所有的utils
### 用例生成
- [x] 人工测试用例
- [x] randoop与evosuite
- [x] 测试用例静态插桩
  - [ ] 在每个测试用例执行的第一行 print出包名、类名、方法名
### 插桩
- [x] jvm动态插桩
    - [x] 修改jacoco
    - [x] 区分NORMAL桩和JUMP桩
- [x] 修改build文件 插桩
### 用例执行
- [ ] 仅执行相关测试用例，从文件defects4j/projects/[proj_id]/relevant_tests/[version_num] 中查找相关测试用例；
- [x] 执行用例 获取数据
- [x] 编写进程池
- [x] 执行变异测试
- [ ] 编写执行脚本
    - [ ] 执行所有version 获取日志信息
    - [x] 多线程
    - [x] 断点续传

### 日志分析

- [x] 编写testcase类
  - [x] 统计cover的所有probe
  - [x] 桩信息probe类
    - [x] 桩类别（NORMAL、JUMP）
    - [x] 每个桩子被testcase覆盖的信息
  - [ ] testcase的冗余信息
    - [ ] （CaCl冗余）testCase相对于testClass的冗余
    - [ ] （CaS冗余）testCase相对于testSuite的冗余
- [x] 编写testclass类
  - [x] 包含的testcase列表
  - [x] 统计cover的所有probe
  - [ ] testclass冗余信息
    - [ ] （ClS冗余）testClass相对于testSuite的冗余
- [x] 编写testsuite类
  - [x] 包含的testclass列表
  - [x] 统计插桩的probe总数
  - [x] 统计cover的所有probe
  - [ ] 变异测试结果
- [ ] 对象序列化
  - [ ] 避免重复计算