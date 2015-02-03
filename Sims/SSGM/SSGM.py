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
          self.not_quiet = True
          self.display = True
          self.d_steps = 1000
          
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
     
     def is_valid_move(self,coords):
          danger_zone = (2.0 * self.rad_spheres) ** 2.0
          imax = len(self.spheres) - 1
          imin = 0
          while imax > imin:
               imid = (imax + imin) / 2
               
               if self.spheres[imid] < coords:
                    imin = imid + 1
               else:
                    imax = imid - 1
                    
          imid = imin
          
          coord_0 = coords[0]
          #check up list
          curr = imid
          coord_c = coord_0
          while coord_c - coord_0 < 2.0 * self.rad_spheres:
               d0 = self.spheres[curr].calc_dist_sq(coords)
               if d0 < danger_zone:
                    return False, imid
               curr += 1
               if not curr < len(self.spheres):
                    break
               coord_c = self.spheres[curr].coords[0]
          #check down list
          curr = imid
          coord_c = coord_0
          while coord_0 - coord_c < 2.0 * self.rad_spheres:
               d0 = self.spheres[curr].calc_dist_sq(coords)
               if d0 < danger_zone:
                    return False, imid
               curr -= 1
               if not curr >= 0:
                    break
               coord_c = self.spheres[curr].coords[0]
               if coord_c == -1:
                    break
          if self.spheres[imid] < coords:
               return True, imid + 1
          else:
               return True, imid
                    
     def mix(self,t=1000):
          if self.display:
               import matplotlib.pyplot as plt
               from matplotlib.pyplot import Figure, subplot
               fig=plt.figure(1)
               plt.axis([0,1,0,1])
               ax=fig.add_subplot(1,1,1)
               ax.set_aspect('equal')
               
               CIRCLES = []
               
               for s in self.spheres:
                    temp_c = plt.Circle(s.coords, radius=s.radius, color='g', fill=True)
                    CIRCLES.append(temp_c)
                    ax.add_patch(temp_c)
               
               plt.show(block=False)
          t0 = 0
          box_buffer = 1 - 2 * self.rad_spheres
          while t0 < t:
               i = randint(0,len(self)-1)
               temp = self.spheres[i]
               del(self.spheres[i])
               r_coords = []
               for r in range(self.num_dims):
                    r_coords.append(box_buffer * random() + self.rad_spheres)
               
               valid, index = self.is_valid_move(r_coords)
               if valid:
                    self.spheres.insert(index,sphere(self.rad_spheres,r_coords,temp.label))
                    if self.display:
                         circ_index = int(self.spheres[index].label)
                         CIRCLES[circ_index].center = r_coords
               else:
                    self.spheres.insert(i,temp)
               del(temp)
               
               self.timesteps += 1
               t0 += 1
               
               if self.display and self.timesteps % self.d_steps == 0:
                   plt.draw()
                    
               if self.pfile and self.timesteps % self.p_steps == 0:
                    dump(self, open( self.pfile, "wb" ))
                    if self.not_quiet:
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
                 
     parser.add_option("-q", "--quiet",
                  action="store_false", default=True,
                  help="turns OFF all display")
               
     parser.add_option("-d", "--display",
                  action="store_true", default=False,
                  help="turns ON graphics")
                   
     parser.add_option("--d_step", metavar='VAR',
                  action="store", type="int", default=500,
                  help="change when display window updates, default is 500")
                  
     (options, args) = parser.parse_args()
     
     t = options.timesteps
     load_name = options.picklefile
     show_display = options.display
     not_quiet = options.quiet
     picklename = options.filename
     save_int = options.saveinterval
     disp_int = options.d_step
     
     if not load_name:
          num_spheres = options.numspheres
          rho = options.rho
          
          BOX = ssgm(num_spheres, rho=rho)
     
     else:
          BOX = load(open( load_name, "rb" ))
     
     BOX.pfile = picklename
     BOX.p_steps = save_int
     BOX.not_quiet = not_quiet
     BOX.display = show_display
     BOX.d_steps = disp_int  
     BOX.mix(t)
     
     if not_quiet:
          
          print BOX
          
          if show_display:
               import matplotlib.pyplot as plt
               from matplotlib.pyplot import Figure, subplot
               
               fig=plt.figure(1)
               plt.axis([0,1,0,1])
               ax=fig.add_subplot(1,1,1)
               ax.set_aspect('equal')
               
               for s in BOX.spheres:
                    ax.add_patch(plt.Circle(s.coords, radius=s.radius, color='g', fill=True))
               
               plt.show()
