import CloudFlare
import csv
import requests
import os.path
from remove_fail_ip import tg_api, bot_token, chat_id, tg_msg_tmp, cf_email, cf_api, domain_name, zone_id

# 初始化一个空列表来保存 IP 地址
ip_list = []
latency_list = []
speed_list = []

file_path = 'result.csv'

if os.path.exists(file_path):
  result_path = './result.csv'
else:
  result_path = './cf_ddns/result.csv'

# 打开 CSV 文件进行读取
with open(result_path, newline='', encoding='utf-8') as csvfile:
    # 创建 CSV 读取器
    csv_reader = csv.reader(csvfile)

    # 跳过第一行（标题行）
    next(csv_reader, None)

    # 遍历 CSV 文件的每一行
    for row in csv_reader:
        # 提取第一列的内容并添加到 ip_list 列表中
        ip_address = row[0]
        ip_list.append(ip_address)
        latency = row[4]
        latency_list.append(latency)
        speed = row[5]
        speed_list.append(speed)
        
cf = CloudFlare.CloudFlare(
    email=cf_email,   # 你的CloudFlare邮箱
    token=cf_api    # Global API KEY
)

for index, ip in enumerate(ip_list):
    dns_record = {
        'type': 'A',  # DNS 记录类型，可以是 'A' 或 'AAAA'（IPv6）
        'name': domain_name,  # 你要解析的域名
        'content': ip,  # 优选后的IP 地址，自动从ip_list提取
        'proxied': False  # 是否启用代理
    }
    
    # 获取 Zone 信息
    zone_info = cf.zones.get(zone_id)
    
    # 使用适当的 Cloudflare API 端点来添加 DNS 记录
    try:
        cf.zones.dns_records.post(zone_id, data=dns_record)  # 添加 DNS 记录
        print('DNS 记录已成功添加!IP地址是{}'.format(ip))
        tg_msg = tg_msg_tmp + '【CF】{}的DNS记录已成功添加!\nIP地址是:{}\n延迟是:{}\n速度是{}'.format(domain_name, ip, latency_list[index], speed_list[index])
        r = requests.post(tg_msg)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        print('添加 DNS 记录失败:{}'.format(ip, e))
        tg_msg = tg_msg_tmp + '【CF】{}的DNS记录添加失败!\nIP地址是失败:{} \n原因是{}'.format(domain_name, ip, e)
        r = requests.post(tg_msg)