import numpy as up

'''
输出文件路径
'''
out_path = '/output/solution.txt'
# out_path = './solution.txt'
'''
输出结果
参数: T：时刻数； M:客户节点数； clients：客户节点名； N：边缘节点数； edges：边缘节点名；D,Y:用户需求矩阵； X:分配结果数组
'''
def write(T, M, clients, N, edges, D, Y, X):
    ans = ''
    for i in range(T):
        for j in range(M):
            result = clients[j] + ':'
            if D[i][j] > 0:
                for k in range(len(Y[j])):
                    cur_n = Y[j][k]
                    if X[i * M + j][cur_n] == 0:
                        continue
                    result += '<' + edges[cur_n] + ',' + str(X[i * M + j][cur_n]) + '>,'
            result = result.strip(',')
            ans += result + '\r\n'
    with open(out_path, 'w') as fout:
        fout.write(ans)