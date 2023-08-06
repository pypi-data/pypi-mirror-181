import numpy as np
from sklearn.metrics import roc_curve as rc
from iman import *
import Levenshtein as Lev


def help():
   print('\nneed <Levenshtein> and <sklearn>\n')


def cosine_distance(v1,v2):
  dot_product = np.dot(v1, v2)
  norm_a = np.linalg.norm(v1)
  norm_b = np.linalg.norm(v2)
  return dot_product / (norm_a * norm_b)

def compute_eer(fpr,tpr,thresholds):
    fnr = 1-tpr
    abs_diffs = np.abs(fpr - fnr)
    min_index = np.argmin(abs_diffs)
    eer = np.mean((fpr[min_index], fnr[min_index]))
    return eer, thresholds[min_index]  ,min_index

def compute_FR(x , fpr, tpr):
    abs_diffs = np.abs(fpr*100 - x)  
    minval = np.min(abs_diffs)  
    aaa = np.where(abs_diffs == minval)  
    min_index = aaa[0][len(aaa[0])-1]
    fr = 1 - tpr[min_index]
    return fr

def EER(y, y_pred, pos_label=1): 
   fpr, tpr, threshold = rc(np.array(y), np.array(y_pred), pos_label=pos_label)
   eer , th,t =  compute_eer(fpr,tpr,threshold)
   fnr = 1-tpr
   recall = tpr / (tpr+fnr) 
   pre = tpr / (tpr + fpr)  
   fm = (2*recall*pre)   /(recall+pre)
   print("fpr , fnr , threshold , eer , th,t , recall , pre,fm")
   return (fpr , fnr , threshold , eer , th,t , recall , pre,fm)   
 
def roc(y , y_pred , pos_label=1):
    fpr , fnr , threshold ,eer , th,_,_,_,_=  EER(y , y_pred , pos_label=pos_label) 
    plt.figure()
    plt.title('EER=' + F(eer,2) + '   th=' + F(th,5))
    plt.plot(threshold,fpr )
    plt.plot(threshold,fnr )
    plt.show()
    print("fpr , fnr , threshold , eer , th")
    return (fpr , fnr , threshold , eer , th)  


def cer(ref, hyp):
    ref = ref.replace(' ', '').replace('‌','')
    hyp = hyp.replace(' ', '').replace('‌','')
    return Lev.distance(ref, hyp)/len(ref)

def wer(ref, hyp):
    ref = ref.replace('‌','')
    hyp = hyp.replace('‌','')
    b = set(ref.split() + hyp.split())
    word2char = dict(zip(b, range(len(b))))
    w1 = [chr(word2char[w]) for w in ref.split()]
    w2 = [chr(word2char[w]) for w in hyp.split()]
    return Lev.distance(''.join(w1), ''.join(w2)) / len(ref.split())
    
def wer_list(ref_list , hyp_list):
    x=[]
    for i in range(len(ref_list)):
       x.append(wer(ref_list[i] , hyp_list[i]))
    return np.mean(x)   
    
def cer_list(ref_list , hyp_list):
    x=[]
    for i in range(len(ref_list)):
       x.append(cer(ref_list[i] , hyp_list[i]))
    return np.mean(x)    