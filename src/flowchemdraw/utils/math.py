import numpy as np

def xy(r,phi, pos=(0,0)):
  return pos[0] + r*np.cos(phi), pos[1] + r*np.sin(phi)

def dist_points(P1: tuple, P2: tuple) -> float:
  return np.sqrt((P1[0]-P2[0])**2 + (P1[1]-P2[1])**2)

def ellipse(a, b, phi, pos=(0,0)):
  return pos[0] + a*np.cos(phi), pos[1] + b*np.sin(phi)