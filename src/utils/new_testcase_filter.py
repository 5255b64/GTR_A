# TODO 重构 忘了这个代码是做什么的
import copy
import random

from math import floor


def main():
    result_dict, result_list = generate4path("cstp.json", 2, 3)
    print(result_dict)
    print(result_list)


def generate4path(predicted_cluster: list, testcase_name: list, case_num: int, is_random=False):
    """
    计算所需的数据
    :param predicted_cluster:
    :param testcase_name:
    :param case_num:
    :param is_random:
    :return:
    """
    # attr, expected_cluster, attr_meaning, testcase_name = extract_path_attr(json_file_path)
    # predicted_cluster = classifier.run(attr, expected_cluster, cluster_num)
    # 存储分类结果
    # 校验参数case_num 要满足生成测试样例数小于总的测试样例数
    if case_num > len(predicted_cluster):
        print("生成的样例数量应该超过总的样例数量 将case_num取为测试用例数量上限" + str(len(predicted_cluster)))
        case_num = len(predicted_cluster)
        # return False, False
    # 声明输出变量
    result_dict = dict()  # 输出结果为一个字典 代表每个类别应该选择的测试样例数量
    result_list = []  # 该结果为list方式 列出所有选择出来的测试样例
    # 初始化输出变量
    for key in predicted_cluster:
        result_dict[key] = []  # 初始化为空的list
    # 根据结果对数据分类
    clusters = dict()
    for i in range(len(predicted_cluster)):
        result = predicted_cluster[i]
        if result not in clusters.keys():
            clusters[result] = []
        clusters[result].append(testcase_name[i])
    # print(clusters)
    # 构建临时字典 挨个删除临时字典内的值 从而生成新的数据集
    temp_clusters = copy.deepcopy(clusters)
    # 目前是按照迭代器的顺序来筛选 应该使用更好的筛选方式
    flag = False
    while ~flag and len(result_list) < case_num:
        for key in temp_clusters.keys():
            if ~flag and len(temp_clusters[key]) > 0:
                if is_random:
                    temp_testcase = temp_clusters[key].pop(floor(random.uniform(0, len(temp_clusters[key]))))  # 会引入随机因素
                else:
                    temp_testcase = temp_clusters[key].pop(0)  # 不会引入随机因素
                result_dict[key].append(temp_testcase)
                result_list.append(temp_testcase)
                if len(result_list) >= case_num:
                    flag = True
                    break
    return result_dict, result_list


if __name__ == "__main__":
    main()
