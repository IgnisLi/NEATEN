import numpy as np
import time
import random
import extraction

# 方案2
# 初始化生成矩阵B
def generate_B(b,z):
    #b = np.random.random(n)
    bz = np.random.random(z)
    bn = np.array(b**2).sum()  # 计算矩阵的第n+1个值
    x = np.diag(np.hstack((b,bn*(-0.5),1,bz)))   # 将矩阵B转化为对角阵
    #print(x)
    return x

# 初始化生成指纹Q
def generate_Q(q,z):
    #q = np.random.random(n)
    rc = np.random.normal(0,0.01,1)
    u = np.array(random.sample(range(z),random.randint(0,z))) # 随机生成小于Z的数组，数组大小为0-z,数组元素值为0-z
    qz = np.zeros(z)
    i = 0
    while i<u.size:
        qz[u[i]] = 1
        i=i+1
    x = np.hstack((q,1,rc,qz))   # 将矩阵B转化为对角阵
    #print(x)
    return x

# step1 随机生成(n+2)*(n+2)的可逆矩阵M1和M2
def initialize(n,z):
    while True:
        m1 = np.random.random((n+2+z,n+2+z))
        #print(len(m1[0]))
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

# step4 接收指纹qc,将扩展为（n+2+z）维的Qc加密，对H加密
def encrypt_fingerprint_q(q,m1,m2,h,z):
    Q = generate_Q(q, z)
    cf = np.matmul(Q,m1)# cf = Q * M1
    Inverse_m2 = np.linalg.inv(m2)
    ch = np.matmul(Inverse_m2,h.T) # ch = M2的逆 * (H)T
    q_sum = np.sum(np.square(q))
    #print(cf)
    #print(ch)
    return cf,ch,q_sum

# step5 计算相似度Pi Pi = CF * Ci * CH
def calculate_Pi(cf,c,ch):
    p = np.matmul(cf,c)
    p = np.matmul(p,ch)
    return p

def cal_encrypt_finger(finger,z):
    n = len(finger)
    B = generate_B(finger, z)  # 注册指码向量
    print('初始化生成秘钥...')
    s1 = time.time()
    M1, M2 = initialize(n, z)
    H, D = generate_A(n, B, z)
    e1 = time.time()
    print('秘钥生成结束，用时：', str(e1 - s1) + '秒')
    print('注册声纹加密...')
    s2 = time.time()
    C = encrypt_D(M1, M2, D)
    e2 = time.time()
    print('注册声纹加密结束，用时：', str(e2 - s2) + '秒')
    return M1,M2,C,H

def cal_comparision(CF,CH,C,q_sum):
    # Q = generate_Q(q, z)
    # CF, CH = encrypt_fingerprint(Q, M1, M2, H)
    pi = calculate_Pi(CF, C, CH)
    print("1111111111:",(pi - q_sum / 2) * (-2))
    P = np.sqrt(abs((pi - q_sum / 2) * (-2)))
    return P


start = time.time()
z = 1# 将指纹向量扩展为(z+n+2) z为随机数 z>=1
print('声音预处理...')
s3 = time.time()
#需要提取的语音文件
filename = '666&&1.wav'
title= filename[:-4]
print(title)
identifier = title.split("&&")
print(identifier)
result1=''
success=True
flag = identifier[1]
e3 = time.time()
print('声音预处理结束，用时：', str(e3 - s3) + '秒')
print('预处理得到的声音文件：', filename)
print('声纹模板提取...')
s2 = time.time()
voiceprint_a = extraction.ertract_voiceprint(filename, sr=16000)
print("3333333",type(voiceprint_a))
# if os.path.exists('666_reg.npy'):
#     os.remove('666_reg.npy')
#     print("delete 666_reg.npy")
np.save('666_login.npy',voiceprint_a)
e2 = time.time()
print('声纹模板提取结束，用时：',str(e2-s2)+'秒')
a = voiceprint_a.cpu().numpy().tolist()[0]
print('提取出的声纹模板：',a)

print('注册声纹模板读取...')
voiceprint_b = np.load('666_reg.npy')
# s2 = time.time()
# voiceprint_b = client_package.extraction.ertract_voiceprint(filename1, sr=16000)
# e2 = time.time()
# print('声纹模板提取结束，用时：',str(e2-s2)+'秒')
b = voiceprint_b.tolist()[0]
print('提取出的声纹模板：',b)

print('注册声纹模板读取...')
voiceprint_a = np.load('666_login.npy')
# s2 = time.time()
# voiceprint_b = client_package.extraction.ertract_voiceprint(filename1, sr=16000)
# e2 = time.time()
# print('声纹模板提取结束，用时：',str(e2-s2)+'秒')
a = voiceprint_a.tolist()[0]
print('提取出的声纹模板：',a)


M1,M2,C,H = cal_encrypt_finger(np.array(b),z)
print("M1:",M1)
print("M2:",M2)
print("C:",C)
print("H:",H)
CF, CH, q_sum = encrypt_fingerprint_q(np.array(a), M1, M2, H, z)
print("CF",CF)
print("CH",CH)
print("q_sum:",q_sum)
p = cal_comparision(CF,CH,C,q_sum)
#p = np.sqrt((pi -np.sum(np.square(q))/2)*(-2))
print('pi:',p)
p = cal_comparision(CF,CH,C,q_sum)
#p = np.sqrt((pi -np.sum(np.square(q))/2)*(-2))
print('pi:',p)
op1=np.sqrt(np.sum(np.square(np.array(b)-np.array(a))))

print('op1:',op1)


