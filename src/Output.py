import numpy as up

'''
输出文件路径
'''
out_path = './solution.txt'

'''
输出结果
参数: T：时刻数； M:客户节点数； clients：客户节点名； N：边缘节点数； edges：边缘节点名； X:分配结果数组
'''
def write(T, M, clients, N, edges, X):
    ans = ''
    for i in range(T):
        for j in range(M):
            result = clients[j] + ':'
            for k in range(N):
                if X[i * M + j][k] == 0:
                    continue
                result += '<' + edges[k] + ',' + str(X[i * M + j][k]) + '>'
            ans += result + '\r\n'
    with open(out_path, 'w') as fout:
        fout.write(ans)