import CloudFlare
import socket
import time
import requests

cf_email = ''   # 你的cloudFlare邮箱
cf_api = '' # Global API KEY

cf = CloudFlare.CloudFlare(
	email=cf_email,
	token=cf_api
)

# 域名和 Zone ID
domain_name = ''  # 你要查询的域名
zone_id = ''  # 你的域名所属的 Zone ID

# tg_bot 参数
tg_api = ''  # 你的TG API，用CF Worker反代后可以在墙内使用
bot_token = ''
chat_id = ''

tg_msg_tmp = 'https://{}/bot{}/sendMessage?chat_id={}&text='.format(tg_api, bot_token, chat_id)

# 获取特定域名的 DNS 解析记录
dns_records = cf.zones.dns_records.get(zone_id, params={'name': domain_name})

success = 0
fail = 0

# 打印 DNS 解析记录
for index, record in enumerate(dns_records):
	host = record['content']
	print(record['content'])
	# print(f"Type: {record['type']}, Name: {record['name']}, Content: {record['content']}")
	
	port = 443  # 替换为要测试的端口号
	try:
		# 创建一个 IPv4 的 socket
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# 设置超时时间（秒）
		client_socket.settimeout(1)
		
		# 记录开始时间
		start_time = time.time()
		
		# 尝试连接到目标主机和端口
		client_socket.connect((host, port))
		
		# 计算连接建立所需的时间
		end_time = time.time()
		elapsed_time = (end_time - start_time) * 1000
		
		# 如果连接成功，表示主机和端口可达
		print(f'TCP Ping {host}:{port} 成功！')
		print(f'连接建立时间：{elapsed_time:.1f} 豪秒')
		success += 1
	except Exception as e:
		print(f'TCP Ping {host}:{port} 失败：{e}')
		try:
			cf.zones.dns_records.delete(zone_id, record['id'])  # 删除符合条件的 DNS 记录
			print(f'DNS 记录已成功删除! IP 地址 {host}')
			tg_msg = tg_msg_tmp + 'DNS 记录已成功删除! IP 地址 {}'.format(host)
			r = requests.post(tg_msg)
			fail += 1
		except CloudFlare.exceptions.CloudFlareAPIError as e:
			print('删除 DNS 记录失败:', e)
			tg_msg = tg_msg_tmp + '删除 DNS 记录失败: {}'.format(e)
			break  # 如果删除失败，可能需要采取适当的处理，此处选择退出循环
	finally:
		# 关闭 socket 连接
		client_socket.close()

msg = '当前共有优选ip{}个，有效{}个，失效删除{}个'.format(len(dns_records), success, fail)
tg_msg = tg_msg_tmp + msg
r = requests.post(tg_msg)
