# Sphere.py
from math import pi

class sphere:

     def __init__(self,r,c=[],l=None):
          self.radius = r
          self.coords = c
          self.label = l
     
     def __len__(self):
          return len(self.coords)
     
     def __getitem__(self,i):
          return self.coords[i]
     
     def get_coords(self):
          return self.coords
     
     def get_radius(self):
          return self.radius
     
     def __repr__(self):
          x = ''
          if self.label:
               x += "Label:  " + str(self.label) + '\n'
          x += "Radius: " + str(self.radius) + '\n'
          x += "Coords: " + str(self.coords)
          return x
     
     def vol(self):
          if len(self.coords) == 2:
               return pi * (self.radius ** 2)
          elif len(self.coords) == 3:
               return (4.0/3.0) * pi * (self.radius ** 3)
     
     def calc_dist_sq(self,other):
          if len(other) != len(self.coords):
               raise Exception("Dimension mismatch")
               
          d = 0.0
          for c in range(len(other)):
               d += (other[c] - self.coords[c]) ** 2.0
          return d
     
     def __lt__(self,coords):
          if len(coords) != len(self.coords):
               raise Exception("Dimension mismatch")
               
          for i in range(len(self.coords)):
               if self.coords[i] < coords[i]:
                    return True
               elif self.coords[i] > coords[i]:
                    return False
          
          return False
               
     
     def __gt__(self,coords):
          if len(coords) != len(self.coords):
               raise Exception("Dimension mismatch")
               
          for i in range(len(self.coords)):
               if self.coords[i] > coords[i]:
                    return True
               elif self.coords[i] < coords[i]:
                    return False
          
          return False
     
     def __eq__(self,coords):
          if len(coords) != len(self.coords):
               raise Exception("Dimension mismatch")
          for i in range(len(self.coords)):
               if self.coords[i] != coords[i]:
                    return False
          return True
