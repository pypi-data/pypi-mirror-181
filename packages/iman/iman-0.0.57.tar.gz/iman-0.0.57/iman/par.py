from multiprocessing import Pool
from functools import partial


def par(files , func , worker=4 , args=[]):
  with Pool(processes=worker) as pool:
     out_res = pool.map(partial(fun, b=args), files)
  return  out_res 

  