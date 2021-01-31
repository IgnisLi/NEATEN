import numpy as np
import time
import random

# 方案2
# 初始化生成矩阵B
def generate_B(b,z):
    #b = np.random.random(n)
    # bz = np.random.random(z)
    bz=np.random.normal(0, 0.1, z)
    bn = np.array(b**2).sum()  # 计算矩阵的第n+1个值
    x = np.diag(np.hstack((b,bn*(-0.5),1,bz)))   # 将矩阵B转化为对角阵
    #print(x)
    return x

# 初始化生成指纹Q
def generate_Q(q,z):
    #q = np.random.random(n)
    rc = np.random.normal(0,0.1,1)
    # u = np.array(random.sample(range(z),random.randint(0,z))) # 随机生成小于Z的数组，数组大小为0-z,数组元素值为0-z
    # qz = np.zeros(z)
    # i = 0
    # while i<u.size:
    #     qz[u[i]] = 1
    #     i=i+1
    qz=np.random.normal(0,0.1,z)
    x = np.hstack((q,1,rc,qz))   # 将矩阵B转化为对角阵
    #print(x)
    return x

# step1 随机生成(n+2)*(n+2)的可逆矩阵M1和M2
def initialize(n,z):
    while True:
        m1 = np.random.random((n+2+z,n+2+z))
        if np.linalg.det(m1)>0:
            break
    while True:
        m2 = np.random.random((n+2+z,n+2+z))
        if np.linalg.det(m2)>0:
            break
    return m1,m2

# step2 随机生成(n+2)*(n+2)的矩阵A，根据Ai生成矩阵H，Ai*(H)T = 1 Di*(H)T = (Bi)T  所以Di = (bi)T * A
def generate_A(n,b,z):
    a = np.random.random((n+2+z,n+2+z))
    one = np.ones(n+2+z)
    ht = np.linalg.solve(a,one)
    h = ht.T
    d = np.matmul(b,a)
    b1 = np.matmul(d,ht)
    #print(b1)
    #print(b)
    return h,d

# step3 加密Di 加密后的C= M1的逆 * Di * M2
def encrypt_D(m1,m2,d):
    Inverse_m1 = np.linalg.inv(m1)
    c = np.matmul(Inverse_m1,d)
    c = np.matmul(c,m2)
    #print('c=',c)
    return c

# step4 接收指纹qc,将扩展为（n+2）维的Qc加密，对H加密
def encrypt_fingerprint(q,m1,m2,h):
    #cf = np.matmul(q,m1)# cf = Q * M1
    Inverse_m2 = np.linalg.inv(m2)
    ch = np.matmul(Inverse_m2,h.T) # ch = M2的逆 * (H)T
    #print(cf)
    #print(ch)
    return ch

# step5 计算相似度Pi Pi = CF * Ci * CH
def calculate_Pi(cf,c,ch):
    p = np.matmul(cf,c)
    p = np.matmul(p,ch)
    return p

def cal_encrypt_finger(finger,z):
    n = len(finger)
    s1 = time.time()
    B = generate_B(finger, z)  # 注册指码向量
    M1, M2 = initialize(n, z)
    H, D = generate_A(n, B, z)
    e1 = time.time()
    #print('生成秘钥的用时：', str(e1 - s1) + '秒')
    s2 = time.time()
    C = encrypt_D(M1, M2, D)
    e2 = time.time()
    #print('加密注册声纹模板的用时：', str(e2 - s2) + '秒')
    return M1,M2,C,H

def cal_comparision(q,z,H,M1,M2,C):

    rzs=time.time()
    Q = generate_Q(q, z)
    CH = encrypt_fingerprint(Q, M1, M2, H)
    rze = time.time()
    #print('加密认证声纹模板的用时：', str(rze - rzs) + '秒')
    ous=time.time()
    CF = np.matmul(q,M1)# cf = Q * M1
    pi = calculate_Pi(CF, C, CH)
    P = np.sqrt((pi - (np.sum(np.square(q))+2*Q[-2]) / 2) * (-2))
    oue=time.time()
    #print('相似度计算用时：', str(oue - ous) + '秒')
    return P,CF


#start = time.time()
i =0
sum =0
while(i<100):
    z = 1# 将指纹向量扩展为(z+n+2) z为随机数 z>=1
    n = 200
    #b = np.array([1,2,3])
    b = np.random.random(n)
    #print("b:",b)

    M1,M2,C,H = cal_encrypt_finger(b,z)
    #q = np.array(150)
    q = np.random.random(n)

    #pi,CF = cal_comparision(q,z,H,M1,M2,C)
    Q = generate_Q(q, z)
    CH = encrypt_fingerprint(Q, M1, M2, H)

    # print('加密认证声纹模板的用时：', str(rze - rzs) + '秒')
    s1 = time.time()
    CF = np.matmul(Q, M1)  # cf = Q * M1
    pi = calculate_Pi(CF, C, CH)
    P = np.sqrt((pi - (np.sum(np.square(q)) + 2 * Q[-2]) / 2) * (-2))
    #p = np.sqrt((pi -np.sum(np.square(q))/2)*(-2))

    e1 =time.time()
    print('pi:',pi)
    result = e1-s1
    #print(result)
    sum = sum+result
    # op1=np.sqrt(np.sum(np.square(b-q)))
    #
    # print('op1:',op1)
    i+=1

#end = time.time()
print("用时：",str(sum)+'秒')

