import requests
import zipfile
import io
import os
import re


port = 443

# 设置文件的URL
url = 'https://zip.baipiao.eu.org/'  # 将 'your_file.zip' 替换为你要下载的文件的实际URL

# 发起GET请求以下载文件
response = requests.get(url)

# 检查是否成功获取文件
if response.status_code == 200:
    # 提取文件名
    file_name = url.split('/')[-1]

    # 将二进制内容解压缩到当前目录
    with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
    
    print(f'文件 {file_name} 已成功下载并解压到当前目录。')
else:
    print('文件下载失败。')

folder = '.'

result_file = f'ip.txt'

with open(result_file, 'w') as f:
    for filename in os.listdir(folder):
        if re.search(rf'-{port}\.txt$', filename):
            with open(filename) as src:
                f.write(src.read())

# 打开 cf.txt 文件以供读取
with open('cf.txt', 'r') as cf_file:
    cf_content = cf_file.read()

# 打开 ip.txt 文件以供追加
with open('ip.txt', 'a') as ip_file:
    # 将 cf.txt 的内容追加到 ip.txt 的末尾
    ip_file.write(cf_content)

print("cf.txt内容已成功追加到 ip.txt 文件中")



