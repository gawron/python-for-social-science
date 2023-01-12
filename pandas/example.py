import numpy as np
import random


bins = np.array([.08,.10, .12,.14,.16,.18,.21,.25])



def return_index(point):

    return len(bins[bins <= point]) - 1

print(bins)
print('~'*20)

mlist = np.arange(.084, .25, .01)
for i in range(17):
  #m1 = random.uniform(0.08, 0.15)
  print(f'{mlist[i]:.4f}  {return_index(mlist[i])}')
