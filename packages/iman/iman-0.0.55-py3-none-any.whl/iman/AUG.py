from iman import *
from scipy.signal import fftconvolve


def cut_noise(noise , le):
      n=[]
      mle = len(noise)
      if (mle > le):
         return noise[0:le]
      else:
         kt = le//mle    
         for i in range(kt):
             n = np.hstack((n , noise))
         nn = noise[0:le - mle*kt]
         n = np.hstack((n , nn))
         return n
     
def Add_Noise( data , noise , snr=15):
        cutnoise = cut_noise(noise , len(data))
        iPn = 1/np.mean(noise*noise)
        Px = np.mean(data*data)
        Msnr = np.sqrt( 10**(-snr/10) * iPn*Px )
        data_noise = data + cutnoise*Msnr
        return data_noise
 

def Add_Reverb( data , rir):
      return fftconvolve(data,rir)[1000:len(data)+1000]


        
 
        
class aug():
  def __init__(self,sox_path='sox.exe'):
    self.sox_path=sox_path   
  def mp3(self,fname , sr, fout,ratio):
   try:
    mp3name = PN(fname)+'.mp3'
    command='%s -t wav -r %s -c 1 "%s" -t mp3 -r %s "%s"' %(self.sox_path,sr,fname ,ratio , mp3name ) 
    os.system(command)
    command='%s "%s" -r %s "%s"' %(self.sox_path,mp3name,sr ,fout ) 
    os.system(command)
    command='del "%s"' %(mp3name) 
    os.system(command)
    return 1  
   except:
    return 0

  def speed(self,fname,fout,ratio):
   try:
    command='%s "%s" "%s" tempo %s' %(self.sox_path,fname ,fout , ratio)   
    os.system(command) 
    return 1
   except:
     return 0  

  def volume(self,fname ,fout,ratio):
   try:
    command='%s -v %s "%s" "%s"' %(self.sox_path,ratio ,fname ,fout ) 
    os.system(command)
    return 1
   except:
     return 0   
	             
def Add_NoiseT( data , noise , snr=15):
        data = data.squeeze()
        noise = noise.squeeze()
        cutnoise = cut_noise(noise , data.size(0))
        iPn = 1/torch.mean(noise*noise)
        Px = torch.mean(data*data)
        Msnr = torch.sqrt( 10**(-snr/10) * iPn*Px )
        data_noise = data + cutnoise*Msnr
        return data_noise

    
def Add_ReverbT( data , rir):
      data = data.squeeze()
      rir = rir.squeeze()
      return fftconvolve(data,rir)[1000:data.size(0)+1000]                 