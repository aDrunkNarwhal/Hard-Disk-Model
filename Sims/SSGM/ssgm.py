# ssgm.py

from sphere import sphere

class ssgm:
     
     def __init__(self,n,r):
          self.num_spheres = n
          self.rad_spheres = r
          self.spheres = []
          
          for i in range(self.num_spheres):
               self.spheres.append(sphere(self.rad_spheres,[0.0,0.0]))
          
          self.rho = self.num_spheres * self.spheres[0].vol()
     
     def __repr__(self):
          x  = "Num Spheres: " + str(self.num_spheres) + '\n'
          x += "Rad Spheres: " + str(self.rad_spheres) + '\n'
          x += "Rho:         " + str(self.rho)
