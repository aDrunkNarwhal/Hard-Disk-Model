# sphere.py
from math import pi

class sphere:

     def __init__(self,r,c=[],l=None):
          self.radius = r
          self.coords = c
          self.label = l
     
     def __len__(self):
          return len(self.coords)
     
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
