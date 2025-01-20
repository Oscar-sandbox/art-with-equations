# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 19:36:39 2025
@author: oscar
"""
from functools import lru_cache
from multiprocessing import Pool
import numpy as np
import cv2

@lru_cache(1)
def L(s, x, y):
  arg1 = 23**s *20**(-s) *7*(1 + np.cos(10*s))*(np.cos(7*s)*x + np.sin(7*s)*y + 2*np.cos(17*s)) + \
    4*np.cos(23**s * 20**(-s) * 7*(np.cos(7*s)*x + np.sin(7*s)*y)) + 2*np.cos(5*s)

  arg2 = 23**s*20**(-s)*7*(1 + np.cos(10*s))*(np.cos(7*s)*y - np.sin(7*s)*x + 2*np.cos(15*s)) + \
    4*np.cos(23**s * 20**(-s) * 7*(np.cos(8*s)*x + np.sin(8*s)*y)) + 2*np.cos(7*s)

  return np.cos(arg1)*np.cos(arg2)

@lru_cache(1)
def Q(x, y):
  return x - y/3 + 3*np.cos(7*x + 5*y)/50 + np.cos(17*x - 15*y)/200 + np.cos(47*x + 5*y)/400

@lru_cache(1)
def P(x, y):
  return y + x/3 + 3*np.cos(3*y - 5*x)/50 + np.cos(23*x + 10*y)/200 + np.cos(22*y)/400

@lru_cache(1)
def V(x, y):
  return Q(x,y) + (Q(x,y) + 1)**40/2**40

@lru_cache(1)
def C(v):
  arg = abs(v-3) - 1/2
  return np.exp(-np.exp(1000*arg))

@lru_cache(1)
def B(v, u, x, y):
  arg = Q(x,y)**2 + u*(1 + Q(x,y)/2)*abs(P(x,y)) - 1 + E(x,y)/50
  return np.exp(-np.exp(v*arg))

@lru_cache(1)
def T(v, x, y):
  return np.cos(30*V(x,y))**4 + (4 + 30*C(v))*np.cos(30*V(x,y))**40

@lru_cache(1)
def E(x, y): 
  return sum([3/10*(25/26)**s *L(s,x,y) for s in range(1,41)])

@lru_cache(1)
def R(v, x, y):
  arg = abs(19/20*Q(x,y)**2 + 12/5*(1 + Q(x,y)/2)*abs(P(x,y)) - 1) - 3/25 + E(x,y)/20
  return (1 - 13/10*v)*np.sin(30*V(x,y))**12 *np.exp(-np.exp(50*arg))

@lru_cache(1)
def K(x, y):
  arg = abs(4/5*(x - y/2) + Q(x,y)/5 + 97/100 + 1/4*np.sqrt(abs(y + x/2 + 17/100)) - 3/2*(y + x/2 + 3/20)**2) + \
      -1/100 + E(x,y)/500 + (3/4*(x - y/2 + 1))**10 

  return np.exp(-np.exp(400*arg))

@lru_cache(1)
def A(v, x, y):
  arg1 = np.cos(200*Q(x,y) + 50*P(x,y) + np.cos(18*Q(x,y) + 25*P(x,y)))
  arg2 = 2 - 3*C(v)/10 + abs(arg1)*np.sin(30*V(x,y))**4/10 + (5 + 2*C(v))/10*abs(np.cos(30*V(x,y))) + T(v,x,y)
  arg3 = abs(Q(x,y))**3 + arg2*(2 + Q(x,y))/2*abs(P(x,y)) - 1 + (1 - C(v))/5*E(x,y)*np.cos(30*V(x,y))**10
  arg4 = (1 - 3/5*(1 - B(1000,10,x,y))*np.cos(30*V(x,y))**4)*arg3
  return np.exp(-np.exp(-v*arg4))

@lru_cache(1)
def W(x, y):
  tot = 0
  for s in range(1,41):
    arg1 = (50 - 49*A(1000,x,y))*(30 + s)/30*(np.cos(2*s)*Q(x,y) + np.sin(2*s)*P(x,y)) + 2*np.cos(7*s)
    arg2 = (50 - 49*A(1000,x,y))*(30 + s)/30*(np.cos(2*s)*P(x,y) - np.sin(2*s)*Q(x,y)) + 2*np.cos(9*s)
    arg3 = np.cos(arg1)*np.cos(arg2) - 1 + E(x,y)*(1/100 - A(1000,x,y)/105)
    tot += np.exp(-np.exp(-1000*arg3))
  return tot

@lru_cache(1)
def U(v, x, y):
  arg = 3*abs(E(x,y))*(A(3,x,y) - A(40,x,y))*(1 - B(1000,10,x,y)) + 3*B(1000,10,x,y) - 3*B(70,10,x,y) + B(200,15,x,y) - B(100,15,x,y)
  return (44 + 33*v)/3000*(1 - A(40,x,y))*(33 + (100 + 20*P(x,y))*arg)*(1 - K(x,y))

@lru_cache(1)
def N(x, y):
  return 1/20 + 2/5*(5+24*P(x,y))/4*B(1000,10,x,y)*(1 - B(4,10,x,y)) + \
    (1 + 8*P(x,y))/20*B(200,15,x,y)*(11 - 10*B(4,15,x,y)) + E(x,y)/40 + (20 + E(x,y))/20*A(4,x,y) + \
    (3 - 3*B(1000,10,x,y))/10*np.cos(30*V(x,y))**2

@lru_cache(1)
def H(v, x, y):
  arg1 = (4 + 3*v + 10*abs(E(x,y)))/10*K(x,y) + ((7 - v)/5 - A(40,x,y)/8)*W(x,y) + 3*v/40*(1+y) + E(x,y)/50
  arg2 = B(200,15,x,y)/25 + (10 - 13*v)/10*(abs(E(x,y))+1)/2*B(3,60,x,y) + R(v,x,y) + N(x,y)
  arg3 = np.exp(-np.exp(1000*(abs(Q(x,y)) - 1)))
  return arg1 + U(v,x,y)*arg3*arg2

@lru_cache(1)
def F(x):
  arg1 = np.exp(-np.exp(-1000*x))
  arg2 = np.exp(-np.exp(1000*(x-1)))
  return np.floor(255*arg1*abs(x)**arg2)

def rgb(n, m):
  x, y = (m-1050)/850, (651-n)/850
  return F(H(0,x,y)), F(H(1,x,y)), F(H(2,x,y))

if __name__ == '__main__':    
    sy, sx = 1200, 2000
    grid = [(n+1,m+1) for n in range(sy) for m in range(sx)]

    with Pool(processes=16) as pool:
        records = pool.starmap(rgb, grid)   #841s
    
    img = np.array(records, dtype=np.uint8).reshape(sy, sx, 3)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite('img.png', img)



