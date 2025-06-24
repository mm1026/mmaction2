# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from collections import defaultdict
import git
def expand_training_data(data):
    # 按query分组
    query_groups = defaultdict(list)
    for item in data:
        query_groups[item['query']].append(item['pos'][0])  # 假设每个item只有一个pos

    # 生成新的训练数据
    expanded_data = []
    for query, pos_list in query_groups.items():
        # 为每个pos生成新的训练对
        for i in range(len(pos_list)):
            for j in range(len(pos_list)):
                if i != j:  # 避免自己和自己配对
                    new_item = {
                        "query": pos_list[i],
                        "pos": [pos_list[j]],
                        "neg": [""],
                        "prompt": "Retrieve references.",
                        "type": "symmetric_clustering"
                    }
                    expanded_data.append(new_item)

    # 添加原始数据
    expanded_data.extend(data)
    return expanded_data


# 读取原始 JSONL 文件
data = []
with open('nli.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():  # 跳过空行
            data.append(json.loads(line))

# 扩充数据
expanded_data = expand_training_data(data)
print(f"原始数据条数: {len(data)}")
print(f"扩充后数据条数: {len(expanded_data)}")

# 保存扩充后的数据为JSONL格式
with open('thesis_expanded2.jsonl', 'w', encoding='utf-8') as f:
    for item in expanded_data:
        json_str = json.dumps(item, ensure_ascii=False)
        f.write(json_str + "\n")

print("数据扩充完成！结果已保存到 thesis_expanded.jsonl")
