import torch
from model import *
import librosa
import time
#import wave

#import sck

#def init_model():
dim_voiceprint = 512
num_class = 1211
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#print("loading")
#the_model = DeepSpeakerModel()
modelstime=time.time()
speakermodel = DeepSpeakerModel(dim_voiceprint,num_class)
speakermodel.load_state_dict(torch.load('new_deepspeaker_dict.pkl',map_location='cpu'))#.to(device))
speakermodel = speakermodel.to(device)
speakermodel.eval()
modeletime=time.time()
print('模型载入用时：',str(modeletime-modelstime)+'秒')
#
# speakermodel =the_model.load_state_dict(torch.load('new_deepspeaker.pkl', map_location='cpu'))
#print(type(speakermodel))
# print(type(speakermodel))
embedding_size = 512


# print(device)
# print(speakermodel)
def ertract_voiceprint(audiofilename,sr):
    # ==========提取声纹代码(封装成函数，输入audiofilename，输出voiceprint)=========
    # wav文件名
    audio_data, sr = librosa.load(audiofilename, sr=16000, mono=True)
    # 这里增加删除语音文件代码
    frames_features = read_audiotoMFB(audio_data)
    #print(frames_features.shape)
    extract_input = truncatedinputfromMFB(1)
    network_inputs_np = extract_input(frames_features)
    #print(network_inputs_np.shape)
    transformTensor = totensor()
    network_inputs = transformTensor(network_inputs_np)
    #print(network_inputs.size())
    mfcc = torch.FloatTensor(network_inputs).to(device)
    mfcc = torch.unsqueeze(mfcc,0)
    #print(mfcc)
    with torch.no_grad():
        voiceprint = speakermodel(mfcc)

    #随机生成一个512维的tensor数组
    #voiceprint = torch.randn(1,512)
    #print(voiceprint.size())
    return voiceprint

#def judge():
    # flag = sck.identifier[1]
    # voiceprint_a = ertract_voiceprint(sck.filename,sr=16000)
    # if(flag == 0):
    #     save(sck.identifier[0],voiceprint=voiceprint_a)
    # else:
    #     voiceprint_e = findvoice(sck.identifier[0])
    #     Euclideandist = PairwiseDistance(2)
    #     distance = Euclideandist(voiceprint_e, voiceprint_a)
    #     if distance <= 0.71:
    #         ret = True
    #     else:
    #         ret = False


