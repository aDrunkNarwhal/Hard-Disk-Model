# SSGM.py

import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure, subplot
from optparse import OptionParser
from pickle import load,dump
from Sphere import sphere
from random import random,randint
from math import pi

class ssgm:
     
     def __init__(self,n,r=0.15,rho=None,pfile=None,p_steps=10000):
          self.num_spheres = n
          if rho:
               self.rad_spheres = (float(rho) / (float(n) * pi)) ** (0.5)
          else:
               self.rad_spheres = r
               
          self.num_dims = 2
          self.box_width = (2 * self.rad_spheres) + 0.001
          self.num_boxes = int(1.0 / self.box_width)
          if 1.0 % (self.box_width) != 0:
               self.num_boxes += 1
          self.spheres = []
          self.timesteps = 0
          self.pfile = pfile
          self.p_steps = int(p_steps)
          self.not_quiet = True
          self.display = True
          self.d_steps = 1000
          
          i = 0
          x_i = 0.0
          for x in range(self.num_boxes):
               self.spheres.append([])
               x_i = (x + 0.5) * self.box_width
               y_i = 0.5 * self.box_width
               for y in range(self.num_boxes):
                    if y_i < 1 - self.rad_spheres and x_i < 1 - self.rad_spheres and i < self.num_spheres:
                         self.spheres[x].append([sphere(self.rad_spheres,[x_i,y_i],str(i))])
                         i += 1
                    else:
                         self.spheres[x].append([])
                    y_i += self.box_width
                    
          if i < self.num_spheres:
               print "\nWARNING: Not all disks are in the box, only " + str(i) + " disks\n"
          
          self.rho = self.num_spheres * self.spheres[0][0][0].vol()
     
     def __repr__(self):
          x  = "Num Spheres:    " + str(self.num_spheres) + '\n'
          x += "Rad Spheres:    " + str(self.rad_spheres) + '\n'
          x += "Num Dimensions: " + str(self.num_dims) + '\n'
          x += "Rho:            " + str(self.rho) + '\n'
          x += "Timesteps:      " + str(self.timesteps) + '\n'
          
          return x
     
     def __iter__(self):
          for x in range(self.num_boxes):
               for y in range(self.num_boxes):
                    for z in range(len(self.spheres[x][y])):
                         yield self.spheres[x][y][z]
     
     def __len__(self):
          return self.num_spheres
     
     #def __getitem__(self,i):
     #     return self.spheres[i]
     
     #def __setitem__(self,i,s):
     #     self.spheres[i] = s
     
     def is_valid_move(self,coords):
          danger_zone = (2.0 * self.rad_spheres) ** 2.0
          l = [-1,0,1]
          x_0 = int(coords[0] / (self.box_width))
          y_0 = int(coords[1] / (self.box_width))
                              
          for i in l:
               x_t = x_0 + i
               if x_t >= 0 and x_t < self.num_boxes:
                    for j in l:
                         y_t = y_0 + j
                         if y_t >= 0 and y_t < self.num_boxes:
                              s_list = self.spheres[x_t][y_t]
                              for s in s_list:
                                   d = s.calc_dist_sq(coords)
                                   if d < danger_zone:
                                        return False, None, None
          return True, x_0, y_0
          
                    
     def mix(self,t=1000):
          if self.display and self.not_quiet:
               fig=plt.figure(1)
               plt.axis([0,1,0,1])
               ax=fig.add_subplot(1,1,1)
               ax.set_aspect('equal')
               
               CIRCLES = [None] * self.num_spheres
               
               for s in self:
                    if s:
                         temp_c = plt.Circle(s.coords, radius=s.radius, color='g', fill=True)
                         CIRCLES[int(s.label)] = temp_c
                         ax.add_patch(temp_c)
               
               plt.show(block=False)
          t0 = 0
          box_buffer = 1 - 2 * self.rad_spheres
          while t0 < t:
               x_i = randint(0,self.num_boxes-1)
               y_i = randint(0,self.num_boxes-1)
               while not self.spheres[x_i][y_i]:
                    x_i = randint(0,self.num_boxes-1)
                    y_i = randint(0,self.num_boxes-1)
               
               z_i = randint(0,len(self.spheres[x_i][y_i])-1)
               
               temp_s = self.spheres[x_i][y_i][z_i]
               del(self.spheres[x_i][y_i][z_i])
               
               r_coords = []
               for r in range(self.num_dims):
                    r_coords.append(box_buffer * random() + self.rad_spheres)
               
               valid, x_new, y_new = self.is_valid_move(r_coords)
               
               if valid:
                    self.spheres[x_new][y_new].append(sphere(self.rad_spheres,r_coords,temp_s.label))
                    if self.display:
                         circ_index = int(temp_s.label)
                         CIRCLES[circ_index].center = r_coords
               else:
                    self.spheres[x_i][y_i].append(sphere(self.rad_spheres,temp_s.coords,temp_s.label))
               
               del(temp_s)                    
               
               self.timesteps += 1
               t0 += 1
               
               if self.display and self.not_quiet and self.timesteps % self.d_steps == 0:
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
               fig=plt.figure(1)
               plt.axis([0,1,0,1])
               ax=fig.add_subplot(1,1,1)
               ax.set_aspect('equal')
               
               for s in BOX:
                    if s:
                         ax.add_patch(plt.Circle(s.coords, radius=s.radius, color='g', fill=True))
               
               plt.show(block=True)
