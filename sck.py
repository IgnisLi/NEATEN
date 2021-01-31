import socket,time
import extraction
import os
from model import *
from funcs import *
#import InnerProduct
from fingercode2 import cal_encrypt_finger,cal_comparision


# 建立一个服务端

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#server.bind(('localhost',19090)) #绑定要监听的端口
server.bind(('192.168.1.126',19090))
#server.bind(('127.0.0.1',19090))
#server.bind(('10.173.169.159',19090)) #绑定要监听的端口
server.listen(5) #开始监听 表示可以使用五个链接排队
# conn就是客户端链接过来而在服务端为期生成的一个链接实例
#secu = InnerProduct.InnerProduct()
#
x = []
y = []
i = 0
while 1:

    print("waiting message")

    conn, addr = server.accept()  # 等待链接,多个链接的时候就会出现问题,其实返回了两个值
    # stime = time.time()
    # print('当前服务器时间：', str(stime) + '秒')
    #print(conn, addr)
    # conn.setblocking(0)
    conn.settimeout(3)
    # print('开始采集声音...')
    # s1 = time.time()
    title = conn.recv(1024).decode("utf8","ignore") #接收id
    title = title.replace('\n','')
    #filename = '520&&1'
    identifier = title.split("&&")
    #
    filename = str(title) + ".wav"
    #
    data = conn.recv(1024)  #接收数据
    total_data = b''
    total_data +=  data
    #print('total_data:',total_data)
    count = num = len(data)
    #file = open(filename,"wb")

    while True:
        try:
            data = conn.recv(1024)
            total_data += data
            count = len(data)
            #print(data)
            #print(count)
            num += count
        except:
            break
    # e1 = time.time()
    print("receive done")
    # print('接收声音用时：', str(e1 - s1) + '秒')
    # print('采集到的的声音数据：',total_data)
    #print(id)
    #print(total_data)
    #print(num)
    print('声音预处理...')
    # s3 = time.time()
    with open(filename,"wb") as f:
        f.write(total_data)

    # print(total_data.decode())
    # total_data = total_data.decode()
    # total_data = total_data.split('+@+')
    # if len(total_data) == 2:
    #     result = "N"
    # else:
    #     result = "N"
    # print(result)
    # conn.send(result.encode()) #然后再发送数据
    result1=''
    success=True
    flag = identifier[1]
    # e3 = time.time()
    # print('声音预处理结束，用时：',str(e3-s3)+'秒')
    # print('预处理得到的声音文件：',filename)
    print('声纹模板提取...')
    # s2 = time.time()
    voiceprint_a = extraction.ertract_voiceprint(filename,sr=16000)

    # e2 = time.time()
    # print('声纹模板提取用时：', str(e2 - s2) + '秒')
    #print("encryption of voiceprint_a:",torch.round(voiceprint_a*10000+10000))
    #list
    a = voiceprint_a.cpu().numpy().tolist()[0]
    # print('提取出的声纹模板：',np.array(a))
    #a = secu.negative2positive(a)
    #a = secu.float2int(a)
    # print('声纹模板长度：',len(a))
    # print('声纹模板数据类型：',type(a))

    #a = [4,3,2,1]

    #print('C', C)
    #C = []
    if(flag == '0'):
        #torch.Tensor -> list a,取模
        #a = [1,2,3,4]
        #s, C = secu.Step1(a)
        x = voiceprint_a.cpu().numpy().tolist()[0]
        z = 1
        M1,M2,C,H = cal_encrypt_finger(np.array(x),z)
        # print('初始化注册模板加密秘钥M1：',M1)
        # print('初始化注册模板加密秘钥M2：', M2)
        #print('初始化注册模板加密秘钥H：', H)
        print('注册模板密文C：', C)
        #A = torch.norm(voiceprint_a).item()
        #a = [1,2,3,4]
        #s,C = secu.Step1(a)
        #save(identifier[0],voiceprint=voiceprint_a)
        # datasave_start = time.time()
        save(identifier[0], C, M1, M2, H)
        # datasave_end = time.time()
        # print('向数据库中存储数据的时间：', str(datasave_end - datasave_start) + '秒')
        #file_s = identifier[0] + '.txt'
        #s = str(s)
        # with open(file_s,"w") as f:
        #     f.write(s)

        result1='Y'
    else:
        y = voiceprint_a.cpu().numpy().tolist()[0]
        # torch.Tensor -> list b，取模
        #print('identifier id:',identifier[0])
        #voiceprint_e = findvoice(identifier[0])
        #print("encryption of voiceprint_e:",torch.round(10000-voiceprint_a*10000))
        #Euclideandist = PairwiseDistance(2)
        #distance = Euclideandist(voiceprint_e, voiceprint_a)
        #b = a
        #B = torch.norm(voiceprint_a).item()
        # 从数据库读取C
        # datafind_start = time.time()
        C, M1, M2, H = findvoice(identifier[0])
        # datafind_end = time.time()
        # print('向数据库中取出数据用时：', str(datafind_end - datafind_start) + '秒')
        print("C:", C)
        z = 1
        p,CF =cal_comparision(np.array(y), z, H, M1, M2, C)
        # print('认证模板密文CF：', CF)
        print("两个模板密文比对的相似度P:",p)
        # 从文件中读取s
        # with open(identifier[0] + ".txt") as f:
        #     s = int(f.read())
        #DSum = secu.Step2(b,C)
        #innerproduct = secu.Step3(DSum,s)
        #innerproduct = secu.mul_correct(innerproduct,x,y)
        #print('innerproduct',innerproduct)
        #distance = innerproduct/(A*B)
        #print("distance:",distance)
        if p <= 0.43:
            result1 = "Y"
        else:
            result1 = "N"
            success=False
        login_add(identifier[0],success)
    print(result1)
    conn.send(result1.encode())
    conn.close()
    # etime = time.time()
    # print('服务端用时：', str(etime - stime) + '秒')












