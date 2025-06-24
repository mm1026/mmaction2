
url = "http://127.0.0.1:5000/generate_code"  # 本地地址
# 或 url = "http://192.168.0.16:5000/generate_code"  # 局域网地址

# 准备输入数据
data = {
    "prompt": "Write a Python function to calculate the factorial of a number."
}

# 发送POST请求
response = requests.post(url, json=data)

# 处理响应
if response.status_code == 200:
    result = response.json()
    print("生成的代码:")
    print(result["generated_code"])
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(response.text)
