# Event_Chain.py

import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure, subplot
from optparse import OptionParser
from pickle import load,dump
from Sphere import sphere
from random import random,randint
from math import pi,sin,cos,sqrt

class event_chain:
     
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
                    
          self.slide_dist_org = 0.5
          self.slide_dist = 0.5
          
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
     
     def find_boxes_to_check(self,s,box,slope,dist_left):
          """
          L = [-2,-1,0,1,2]
          x_dir = 1
          if slope[1] < 0:
               x_dir = -1
          y_dir = 1
          if slope[0] < 0:
               y_dir = -1
          
          box_list = []
          curr_box = box
          i = 0
          while self.box_width * i <= self.slide_dist * slope[1]:
               i += 1
               next_box = (curr_box[0] + x_dir,
                           int((line['slope'] * self.box_width * (curr_box[0] + x_dir) + line['y_int']) / self.box_width))
               next_box = tuple([x % self.num_boxes for x in next_box])
               
               last_time = False
               inc_y = curr_box[1]
               while True:
                    if inc_y == next_box[1]:
                         last_time = True
                    for x in L:
                         for y in L:
                              check_box = ((curr_box[0] + x) % self.num_boxes,
                                           (inc_y + y) % self.num_boxes)
                              if check_box not in box_list:
                                   box_list.append(check_box)
                    inc_y = (inc_y + y_dir) % self.num_boxes
                    if last_time:
                         break
               
               curr_box = next_box
                 
          return box_list
          """
          
          box_list = []
          
          return box_list
     
     def slide_sphere(self,s,box,slope,dist_left):
          """
          line = {'slope':slope[0]/slope[1],
                  'y_int':s.coords[1] - slope[0]*s.coords[0]/slope[1]}
          box_list = self.find_boxes_to_check(s,slope,line,box)

          min_sphere = None
          min_box = (0,0)
          min_dist = 100000
          for b in box_list:
               for t_s in self.spheres[b[0]][b[1]]:
                    base = (s.coords[0] - t_s.coords[0]) * slope[1] + (s.coords[1] - t_s.coords[1]) * slope[0]
                    h_sq = t_s.calc_dist_sq(s) - base ** 2.0
                    x = (2.0 * self.rad_spheres) ** 2 - h_sq
                    if x < 0.0 or base < 0.0:
                         continue
                    x = sqrt(x)
                    q = base - x
                    if q < min_dist:
                         min_dist = q
                         min_box = b
                         min_sphere = t_s
          return min_box,min_sphere,min_dist
          """
          
          box_list = self.find_boxes_to_check(s,box,slope,dist_left)  # [{'coords':(int,int),'parity':(a,b)},...]; a,b in [-1,0,1] 
          
          
          
          min_box = (0,0,0)
          min_sphere = None
          min_dist = dist_left
          
          return min_sphere,min_box,min_dist

     def mix(self,t=1000):
          if self.display and self.not_quiet:
               fig=plt.figure(1)
               plt.axis([0,1,0,1])
               ax=fig.add_subplot(1,1,1)
               ax.set_aspect('equal')
               
               CIRCLES = [None] * self.num_spheres * 9
               L = (-1,0,1)
               for s in self:
                    i = 0
                    for x in L:
                         for y in L:
                              temp_c = plt.Circle([s.coords[0] + x,s.coords[1] + y], radius=s.radius, color='g', fill=True)
                              CIRCLES[int(s.label) * 9 + i] = temp_c
                              ax.add_patch(temp_c)
                              i += 1
               
               plt.show(block=False)
          t0 = 0
          while t0 < t:
               x_i = randint(0,self.num_boxes-1)
               y_i = randint(0,self.num_boxes-1)
               while not self.spheres[x_i][y_i]:
                    x_i = randint(0,self.num_boxes-1)
                    y_i = randint(0,self.num_boxes-1)
               
               z_i = randint(0,len(self.spheres[x_i][y_i])-1)
               
               angle = random() * 2 * pi
               slope = (sin(angle),cos(angle))
               
               temp_s = self.spheres[x_i][y_i][z_i]
               del(self.spheres[x_i][y_i][z_i])
               
               dist_left = self.slide_dist
               box = (x_i,y_i)
               while dist_left > 0.0 and temp_s != None:
                    next_sphere,box,dist_traveled = self.slide_sphere(temp_s,box,slope,dist_left)
                    temp_s.coords[0] = (temp_s.coords[0] + slope[1] * dist_traveled) % 1.0
                    temp_s.coords[1] = (temp_s.coords[1] + slope[0] * dist_traveled) % 1.0
                    self.spheres[int(temp_s.coords[0] / self.box_width)][int(temp_s.coords[1] / self.box_width)].append(temp_s)
                    if self.display:
                         circ_index = int(temp_s.label)
                         i = 0
                         for x in L:
                              for y in L:
                                   CIRCLES[circ_index * 9 + i].center = [temp_s.coords[0] + x, temp_s.coords[1] + y]
                                   i += 1
                    temp_s = next_sphere
                    del(next_sphere)
                    dist_left -= dist_traveled      
               
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
     
     parser.add_option("--slide_dist", metavar='VAL',
               action="store", type="float", default=0.5,
               help="modify the the sliding distance for spheres, default is 0.5")
     
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
     s_dist = options.slide_dist
     
     if not load_name:
          num_spheres = options.numspheres
          rho = options.rho
          
          BOX = event_chain(num_spheres, rho=rho)
     
     else:
          BOX = load(open( load_name, "rb" ))
     
     BOX.pfile = picklename
     BOX.p_steps = save_int
     BOX.not_quiet = not_quiet
     BOX.display = show_display
     BOX.d_steps = disp_int 
     BOX.slide_dist = s_dist 
     BOX.mix(t)
     
     if not_quiet:
          
          print BOX
          
          if show_display:
	          plt.show(block=True)
