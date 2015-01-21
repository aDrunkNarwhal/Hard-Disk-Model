# ssgm.py

from sphere import sphere
from random import random,randint
from math import pi
from sys import argv

class ssgm:
     
     def __init__(self,n,r=0.15,rho=None):
          self.num_spheres = n
          if rho:
               self.rad_spheres = (float(rho) / (float(n) * pi)) ** (1.0/2.0)
          else:
               self.rad_spheres = r
               
          self.num_dims = 2
          self.spheres = []
          
          for i in range(self.num_spheres):
               self.spheres.append(sphere(self.rad_spheres,[-1.0,-1.0],str(i)))
          
          self.rho = self.num_spheres * self.spheres[0].vol()
     
     def __repr__(self):
          x  = "Num Spheres:    " + str(self.num_spheres) + '\n'
          x += "Rad Spheres:    " + str(self.rad_spheres) + '\n'
          x += "Num Dimensions: " + str(self.num_dims) + '\n'
          x += "Rho:            " + str(self.rho) + '\n'
          count = 0
          for s in self.spheres:
               if s.coords == [-1.0,-1.0]:
                    count += 1
          x += "Spheres not in: " + str(count)
          return x
     
     def __len__(self):
          return len(self.spheres)
     
     def __getitem__(self,i):
          return self.spheres[i]
     
     def __setitem__(self,i,s):
          self.spheres[i] = s
     
     def is_valid_move(self,index,coords):
          for i in range(len(self.spheres)):
               if i != index:
                    d = 0.0
                    for ci in range(len(coords)):
                         d += (coords[ci] - self.spheres[i].coords[ci]) ** 2
                    if d < (2 * self.rad_spheres) ** 2:
                         return False
          return True
          
     def mix(self,t=1000):
          t0 = 0
          box_buffer = 1 - 2 * self.rad_spheres
          while t0 < t:
               i = randint(0,len(self)-1)
               r_coords = []
               for r in range(self.num_dims):
                    r_coords.append(box_buffer * random() + self.rad_spheres)
               
               if self.is_valid_move(i,r_coords):
                    self.spheres[i].coords = r_coords
               
               t0 += 1

if __name__ == '__main__':
     X = ssgm(100,rho=float(argv[1]))
     X.mix(int(argv[2]))
     print X
     
     import matplotlib.pyplot as plt
     from matplotlib.pyplot import Figure, subplot

     fig=plt.figure(1)
     plt.axis([0,1,0,1])
     ax=fig.add_subplot(1,1,1)
     ax.set_aspect('equal')
     
     for s in X.spheres:
          ax.add_patch(plt.Circle(s.coords, radius=s.radius, color='g', fill=True))
     
     plt.show()
