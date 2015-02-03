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
          
          self.pack_disks()
          
          self.rho = self.num_spheres * self.spheres[0].vol()
     
     def pack_disks(self):
          mini_buff = 0.0001
          edge_buff = self.rad_spheres + mini_buff
          x_inc = (3.0**(1.0/2.0)) * (self.rad_spheres) + mini_buff
          y_inc = 2.0 * self.rad_spheres + mini_buff
          
          index = len(self.spheres) - 1
          x = 1.0 - edge_buff
          y = 1.0 - edge_buff
          y_offset = False
          while index >= 0:
               if y < edge_buff:
                    x -= x_inc
                    y = 1.0 - y_inc
                    if y_offset:
                         y += self.rad_spheres
                         y_offset = False
                    else:
                         y_offset = True
               if x < edge_buff:
                    break
               self.spheres[index].coords = [x,y]
               y -= y_inc
               index -= 1
     
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
                         
     def mix(self,t=1000):
          if self.display and self.not_quiet:
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
               angle = 2 * pi * random()
               
               line = self.gen_line_eq(self.spheres[i],angle)
               
               self.timesteps += 1
               t0 += 1
               
               if self.display and self.not_quiet and self.timesteps % self.d_steps == 0:
                   plt.draw()
                    
               if self.pfile and self.timesteps % self.p_steps == 0:
                    dump(self, open( self.pfile, "wb" ))
                    if self.not_quiet:
                         print "SAVED at timestep:",self.timesteps


     def gen_line_eq(self,point,rads):
          slope = sin(rads) / cos(rads)
          y_int = point[1] - slope * point[0]
          return slope, y_int

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
               
               for s in BOX.spheres:
                    ax.add_patch(plt.Circle(s.coords, radius=s.radius, color='g', fill=True))
               
               plt.show(block=True)
