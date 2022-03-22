import numpy as np
from Input import *
from Output import *


'''
读取输入，初始化数学模型
'''
Q = parse_config(read(config_path))
M, clients, T, D = parse_demand(read(demand_path))
N, edges, C = parse_site_bandwidth(read(site_bandwidth_path))
Y = parse_qos(read(qos_path))

'''
保存分配结果
'''
X = None

'''
分配算法
'''
def main():
    for i in range(len(T)):
        cur_c = C.copy()                                                #边缘节点剩余可分配带宽
        cur_x = np.zeros((M, N), dtype = np.int)                        #存储该时刻分配结果
        for j in range(M):                                              #每时刻单独处理
            available_Q_count = np.sum(Y[...,j] < Q)                    #获取到满足 QoS 约束的边缘节点数量
            up_bound = D[i][j] // available_Q_count                     #需求带宽粗略均分
            excess_traffic = D[i][j] % available_Q_count                #剩余需求
            # print(D[i][j], available_Q_count, up_bound, available_Q_count * up_bound + excess_traffic)
            # count = 0
            for k in range(N):                                          #边缘节点遍历
                if Y[k][j] >= Q:                                        #跳过不满足 QoS 的节点
                    continue
                if excess_traffic > 0 and cur_c[k] > up_bound:          #有剩余需求且当前边缘节点可容纳的情况
                    cur_x[j][k] = cur_x[j][k] + up_bound + 1
                    # count += up_bound + 1
                    cur_c[k] = cur_c[k] - (up_bound + 1)
                    excess_traffic -= 1
                else:                                                   #其他情况
                    cur_x[j][k] += min(cur_c[k], up_bound)
                    # count += min(cur_c[k], up_bound)
                    if cur_c[k] < up_bound:                             #当前边缘几点剩余带宽不足以分配
                        excess_traffic += up_bound - cur_c[k]
                        cur_c[k] = 0
                    else:
                        cur_c[k] -= up_bound
                available_Q_count -= 1
            # print(i, j, excess_traffic, count == D[i][j])
            '''
            对于有剩余的情况保留处理
            '''
            # if excess_traffic > 0:
            #     print(i, j, excess_traffic)
            # break
        if i == 0:                                                      #将分配结果加入X
            X = cur_x
        else:
            X = np.concatenate((X,cur_x))
        # break
    # print(X)
    '''
    写入文件
    '''
    write(len(T), M, clients, N, edges, X)

'''
算法入口
'''
main()