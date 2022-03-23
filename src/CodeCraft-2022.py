import numpy as np
from Input import *
from Output import *
# import time
# import random

# start = time.time()
'''
读取输入，初始化数学模型
'''
Q = parse_config(read(config_path))
M, clients, T, D = parse_demand(read(demand_path))
N, edges, C = parse_site_bandwidth(read(site_bandwidth_path))
Y = parse_qos(read(qos_path), Q, M)

Avar_N = 0

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
            if D[i][j] == 0:
                continue
            # print(len(Y[j]))
            available_Q_count = min(len(Y[j]), Avar_N)                  #获取到满足 QoS 约束的边缘节点数量
            if available_Q_count != 0:
                up_bound = D[i][j] // available_Q_count                     #需求带宽粗略均分
                excess_traffic = D[i][j] % available_Q_count                #剩余需求
            else:
                excess_traffic = D[i][j]                                    #剩余需求
            # print(D[i][j], available_Q_count, up_bound, available_Q_count * up_bound + excess_traffic)
            # count = 0
            for k in range(available_Q_count):                          #边缘节点遍历
                cur_n = Y[j][k]
                if excess_traffic > 0 and cur_c[cur_n] > up_bound:      #有剩余需求且当前边缘节点可容纳的情况
                    cur_x[j][cur_n] += up_bound + 1
                    # count += up_bound + 1
                    cur_c[cur_n] = cur_c[cur_n] - (up_bound + 1)
                    excess_traffic -= 1
                else:                                                   #其他情况
                    cur_x[j][cur_n] += min(cur_c[cur_n], up_bound)
                    # count += min(cur_c[cur_n], up_bound)
                    if cur_c[cur_n] < up_bound:                         #当前边缘几点剩余带宽不足以分配
                        excess_traffic += up_bound - cur_c[cur_n]
                        cur_c[cur_n] = 0
                    else:
                        cur_c[cur_n] -= up_bound
            # print(i, j, excess_traffic, count == D[i][j])
            '''
            对于有剩余的情况保留处理
            '''
            if excess_traffic > 0:
                # print(i, j, excess_traffic)
                for k in range(len(Y[j]) - 1, -1, -1):
                    if excess_traffic == 0:
                        break
                    cur_n = Y[j][k]
                    cur_x[j][cur_n] += min(cur_c[cur_n], excess_traffic)
                    # count += min(cur_c[cur_n], up_bound)
                    if cur_c[cur_n] < excess_traffic:                         #当前边缘几点剩余带宽不足以分配
                        excess_traffic -= cur_c[cur_n]
                        cur_c[cur_n] = 0
                    else:
                        cur_c[cur_n] -= excess_traffic
                        excess_traffic = 0
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
    write(len(T), M, clients, N, edges, D, Y, X)

'''
算法入口
全压测：275.98322057724
273.7613663673401     去掉需求为0的情况
239.22328543663025    main 三重循环 -> 二重循环
235.23891592025757    output 三重循环 -> 二重循环
226.8448293209076     Avar_N
211.7283284664154     shuffle Avar_N = 25
202.54954195022583    shuffle Avar_N = 10
207.21146368980408
'''

# print(time.time() - start)
main()
# print(time.time() - start)