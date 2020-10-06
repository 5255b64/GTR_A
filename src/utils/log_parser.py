# TODO 重构
import json

from src.minimization.attribute_extractor import JSON_FIELD_ID, JSON_FIELD_CASE_NAME, JSON_FIELD_DATA


def parse(input_file_path: str, output_file_path: str):
    # 声明变量
    records: list = list()
    case_num: int = 0
    stake_num: int
    case_stake: list = list()
    test_case: dict
    # 读取文件
    file = open(file=input_file_path, mode="r", encoding="UTF-8")
    for line in file.readlines():
        if line.startswith("testcase:") or line.__contains__("文件写入成功"):
            # 保存旧的数据
            test_case = dict()
            test_case[JSON_FIELD_ID] = case_num
            test_case[JSON_FIELD_CASE_NAME] = "unknown"
            # test_case[JSON_FIELD_DATA] = case_stake
            test_case[JSON_FIELD_DATA] = str(case_stake)
            records.append(test_case)
            # 记录新的case_num
            if line.startswith("testcase:"):
                case_num = int(((line.split("testcase:"))[1].split("\n"))[0])
            # 初始化桩的记录列表
            case_stake = list()
        elif line.__contains__("accurateteststake"):
            stake_num = int((line.split("___"))[1])
            case_stake.append(stake_num)
    # 删除records第一个数据
    records.pop(0)
    result: dict = dict()
    result["RECORDS"] = records
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parse("log.txt", "xxx,json")
