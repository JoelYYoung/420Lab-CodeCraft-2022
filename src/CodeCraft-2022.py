import numpy as np
from Input import *


'''
读取输入，初始化数学模型
'''
Q = parse_config(read(config_path))
M, clients, T, D = parse_demand(read(demand_path))
N, C = parse_site_bandwidth(read(site_bandwidth_path))
Y = parse_qos(read(qos_path))