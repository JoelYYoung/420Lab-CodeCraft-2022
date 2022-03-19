'''
数据文件路径
'''
demand_path = '../../data/demand.csv'
config_path = '../../data/config.ini'
qos_path = '../../data/qos.csv'
site_bandwidth_path = '../../data/site_bandwidth.csv'

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
    return clients

'''
解析客户节点需求
return type: dictionary
return content: time: 当前时刻
                demand: 客户节点需求列表，顺序与客户节点ID列表相同
'''
def parse_demand_body(body):
    body = body.strip()
    words = body.split(',')
    ans = {}
    ans['time'] = words[0]
    ans['demand'] = words[1:]
    return ans

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
    return words[1]

# config = read(config_path)
# print(parse_config(config))

'''
解析边缘节点带宽
return type: dictionary
return content: 字典每一项:key:边缘节点ID; value:该节点贷款上限
'''
def parse_site_bandwidth(lines):
    site_bandwidths = {}
    for i in range(1, len(lines)):
        words = lines[i].strip().split(',')
        site_bandwidths[words[0]] = words[1]
    return site_bandwidths

# site_bandwidth = read(site_bandwidth_path)
# print(parse_site_bandwidth(site_bandwidth))

'''
解析客户节点与边缘节点之间的网络时延
return type: dictionary
return content: key:客户节点ID, value:dictionary
                            key:边缘节点ID, value:两者之间的网络时延
'''
def parse_qos(lines):
    clients = lines[0].strip().split(',')[1:]
    qos = {}
    for i in range(len(clients)):
        qos[clients[i]] = {}
    for i in range(1, len(lines)):
        words = lines[i].strip().split(',')
        site = words[0]
        for j in range(1, len(words)):
            qos[clients[j - 1]][site] = words[j]
    return qos
    
# qos = read(qos_path)
# print(parse_qos(qos)['A'])