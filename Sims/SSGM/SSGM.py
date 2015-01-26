# SSGM.py

from optparse import OptionParser
from pickle import load,dump
from Sphere import sphere
from random import random,randint
from math import pi
from sys import argv

class ssgm:
     
     def __init__(self,n,r=0.15,rho=None,pfile=None,p_steps=10000):
          self.num_spheres = n
          if rho:
               self.rad_spheres = (float(rho) / (float(n) * pi)) ** (1.0/2.0)
          else:
               self.rad_spheres = r
               
          self.num_dims = 2
          self.spheres = []
          self.timesteps = 0
          self.pfile = pfile
          self.p_steps = int(p_steps)
          self.display = True
          
          for i in range(self.num_spheres):
               self.spheres.append(sphere(self.rad_spheres,[-1.0,-1.0],str(i)))
          
          self.rho = self.num_spheres * self.spheres[0].vol()
     
     def __repr__(self):
          x  = "Num Spheres:    " + str(self.num_spheres) + '\n'
          x += "Rad Spheres:    " + str(self.rad_spheres) + '\n'
          x += "Num Dimensions: " + str(self.num_dims) + '\n'
          x += "Rho:            " + str(self.rho) + '\n'
          x += "Timesteps:      " + str(self.timesteps) + '\n'
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
               
               self.timesteps += 1
               t0 += 1
               
               if self.pfile and self.timesteps % self.p_steps == 0:
                    dump(self, open( self.pfile, "wb" ))
                    if self.display:
                         print "SAVED at timestep:",self.timesteps

if __name__ == '__main__':

     parser = OptionParser()
     
     parser.add_option("-n", "--numspheres", metavar='VAL',
               action="store", type="int", default=100,
               help="modify the number of spheres, default is 100")
               
     parser.add_option("-r", "--rho", metavar='VAL',
               action="store", type="float", default=0.7,
               help="modify the the density, default is 0.7")
               
     parser.add_option("-t", "--timesteps", metavar='VAL',
               action="store", type="int", default=1000,
               help="change the number of timesteps it will mix for, default is 1,000")
               
     parser.add_option("-p", "--picklefile", metavar='FILE',
               action="store", type="string", default=None,
               help="import a picklefile")
               
     parser.add_option("-s", "--saveinterval", metavar='VAL',
               action="store", type="int", default=10000,
               help="how many timesteps before a picklefile is saved, default is 10,000")
               
     parser.add_option("-f", "--filename", metavar='FILE',
               action="store", type="string", default='saved.p',
               help="the name of the picklefile to be saved, default is 'saved.p'")
               
     parser.add_option("-d", "--display",
                  action="store_true", default=False,
                  help="turns ON graphics")
                  
     parser.add_option("-q", "--quiet",
                  action="store_false", default=True,
                  help="turns OFF all display")
                  
     (options, args) = parser.parse_args()
     
     t = options.timesteps
     load_name = options.picklefile
     display = options.display
     quiet = options.quiet
     
     if not load_name:
          num_spheres = options.numspheres
          rho = options.rho
          save_int = options.saveinterval
          picklename = options.filename
          
          BOX = ssgm(num_spheres,rho=rho,pfile=picklename,p_steps=save_int)
     
     else:
          BOX = load(open( load_name, "rb" ))
     
     BOX.display = quiet     
     BOX.mix(t)
          
     if quiet:
          
          print BOX
          
          if display:
               import matplotlib.pyplot as plt
               from matplotlib.pyplot import Figure, subplot

               fig=plt.figure(1)
               plt.axis([0,1,0,1])
               ax=fig.add_subplot(1,1,1)
               ax.set_aspect('equal')
               
               for s in BOX.spheres:
                    ax.add_patch(plt.Circle(s.coords, radius=s.radius, color='g', fill=True))
               
               plt.show()
