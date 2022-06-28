import pickle
import numpy as np
w1,voc_index,index_voc,w2 = pickle.load(open('grass.pkl','rb'))

#todo:此处pkl文件是训练好的模型，模型训练真的很花时间，看看能不能去找到现成的训练集


def word_voc(word):
    return w1[voc_index[word]]

def voc_sim(word, top_n):
    v_w1 = word_voc(word)
    word_sim = {}
    for i in range(len(voc_index)):
        v_w2 = w1[i]
        theta_sum = np.dot(v_w1, v_w2)
        theta_den = np.linalg.norm(v_w1) * np.linalg.norm(v_w2)
        theta = theta_sum / theta_den
        word = index_voc[i]
        word_sim[word] = theta
    words_sorted = sorted(word_sim.items(), key=lambda kv: kv[1], reverse=True)
    for word, sim in words_sorted[:top_n]:
        print(word, sim)

if __name__ == '__main__':
    voc_sim('乘法',20)


