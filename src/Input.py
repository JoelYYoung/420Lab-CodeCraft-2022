import numpy as np
import random


'''
数据文件的根路径
'''
root_path = '/data/'

'''
数据文件路径
'''
demand_path = root_path + 'demand.csv'
config_path = root_path + 'config.ini'
qos_path = root_path + 'qos.csv'
site_bandwidth_path = root_path + 'site_bandwidth.csv'

'''
读取文件
return type: list
return content: 文件所有行
'''
def read(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()

'''
解析客户节点需求第一行
return type: list
return content: 客户节点ID列表
'''
def parse_demand_head(head):
    head = head.strip()
    clients = head.split(',')
    clients.pop(0)
    return len(clients), clients

'''
解析客户节点需求
return type: dictionary
return content: time: 当前时刻
                demand: 客户节点需求列表,顺序与客户节点ID列表相同
'''
def parse_demand_line(line):
    line = line.strip()
    words = line.split(',')
    ans = {}
    ans['time'] = words[0]
    ans['demand'] = []
    for i in range(1, len(words)):
        ans['demand'].append(int(words[i]))
    return ans

'''
解析客户节点需求
return type: list, array
return content: 时间戳列表
                需求数组,时间戳*客户节点
'''
def parse_demand_body(body):
    T = []
    D = []
    for i in range(0, len(body)):
        ans = parse_demand_line(body[i])
        T.append(ans['time'])
        D.append(ans['demand'])
    return T, np.array(D)

'''
解析客户节点需求
'''
def parse_demand(demands):
    M, clients = parse_demand_head(demands[0])
    T, D = parse_demand_body(demands[1:])
    return M, clients, T, D

# demands = read(demand_path)
# print(parse_demand_head(demands[0]))
# print(parse_demand_body(demands[1]))

'''
解析参数配置文件
return type: str
return content: QoS约束上限
'''
def parse_config(config):
    words = config[1].strip().split('=')
    return int(words[1])

# config = read(config_path)
# print(parse_config(config))

'''
解析边缘节点带宽
return type: list, array
return content: 边缘节点ID列表
                边缘节点带宽数组
'''
def parse_site_bandwidth(lines):
    N = []
    C = []
    for i in range(1, len(lines)):
        words = lines[i].strip().split(',')
        N.append(words[0])
        C.append(int(words[1]))
    return len(N), N, np.array(C)

# site_bandwidth = read(site_bandwidth_path)
# print(parse_site_bandwidth(site_bandwidth))

'''
解析客户节点与边缘节点之间的网络时延
return type: list(list)
return content: 仅返回满足时延的节点
'''
def parse_qos(lines, Q, M):
    Y = []
    for i in range(M):
        Y.append([])
    for i in range(1, len(lines)):
        words = lines[i].strip().split(',')
        for j in range(1, len(words)):
            if int(words[j]) < Q:
                Y[j - 1].append(i - 1)
            if i == len(lines) - 1:
                random.shuffle(Y[j - 1])
    return Y
    
# qos = read(qos_path)
# print(parse_qos(qos)['A']['A'])