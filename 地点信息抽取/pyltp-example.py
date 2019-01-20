# -*- coding: utf-8 -*-
import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

LTP_DATA_DIR = '/home/zhaoshengjian/下载/ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
results = []

def locationNER(text):
    #先分词
    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型
    words = segmentor.segment(text)  # 分词
    #print ('\t'.join(words))
    segmentor.release()

    #再词性标注
    postagger = Postagger() # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    postagger.release()  # 释放模型

    #最后地理实体识别

    recognizer = NamedEntityRecognizer() # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    for i in range (0,len(netags)):
       if 'I-Ns'in netags[i] or 'I-Ni'in netags[i]:
           results.append(words[i-1]+words[i]+words[i+1])
       if 'S-Ns'in netags[i] or 'S-Ni'in netags[i]:
           results.append(words[i])
    return results



if __name__ == '__main__':
        text = '明天九点从中国科学院大学到怀柔万达广场。'
        locationNER(text)
        for result in results:
            print(result)
