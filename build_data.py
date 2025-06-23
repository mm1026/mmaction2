import mysql.connector
import json
import random
from tqdm import tqdm

# 数据库配置
db_config = {
    "host": "192.168.1.190",
    "port": 3306,
    "user": "root",
    "password": "zkbx@A308",
    "database": "Bibliography"
}

# 读取JSONL文件
input_file = "thesis_expanded2.jsonl"
output_file = "data_expend.jsonl"


def get_random_titles(limit=400000):
    """从数据库获取指定数量的随机标题"""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 使用RAND()函数随机排序并限制数量
    query = f"SELECT title FROM Thesis ORDER BY RAND() LIMIT {limit}"
    cursor.execute(query)

    titles = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return titles


def process_jsonl(all_titles):
    """处理JSONL文件，为每个记录添加neg标题"""
    with open(input_file, "r", encoding="utf-8") as infile, \
            open(output_file, "w", encoding="utf-8") as outfile:

        lines = infile.readlines()
        for line in tqdm(lines, desc="处理JSONL"):
            data = json.loads(line.strip())
            query_title = data["query"]
            pos_titles = data["pos"]

            # 创建排除集：包括query和pos中的所有标题
            exclude_set = set(pos_titles)
            exclude_set.add(query_title)

            # 从所有标题中筛选可用标题
            available_titles = [title for title in all_titles
                                if title not in exclude_set]

            # 随机选择10个标题（保持列表格式）
            if len(available_titles) >= 10:
                selected_neg = random.sample(available_titles, 10)
            else:
                selected_neg = available_titles  # 如果可用标题不足10个

            # 将neg设置为列表
            data["neg"] = selected_neg

            # 写入处理后的数据
            outfile.write(json.dumps(data, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    print("从数据库随机获取40000个标题...")
    all_titles = get_random_titles(limit=400000)
    print(f"获取到 {len(all_titles)} 个标题")

    print("处理JSONL文件...")
    process_jsonl(all_titles)
    print(f"处理完成！结果已保存到 {output_file}")