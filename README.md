<p align="center">
  <img src="img.png" width=100% />
</p>

![License](https://img.shields.io/github/license/Oscar-sandbox/art-with-equations)
![Python version](https://img.shields.io/badge/python-3.11-blue.svg) 

# Art with mathematical equations

## Description
This project constructs an artistic image, depicting a planktonic worm, using only mathematical formulas. 
For each of the 1200x2000 pixels in the image, there are 3 main functions that dictate the RGB values of each pixel. 
In turn, this main functions are entirely defined by an intricate composition of simpler functions, like exponentials, 
sines and cosines. The equations were formulated by Hamid Naderi and originally posted on his [X account](https://x.com/naderi_yeganeh). 
Original post can be seen [here](original_post.png). 

## Code Optimization
A naive approach to coding the equations may lead to a long computation time. First, many of the equations repeatedly call the same 
nested functions with the same inputs. We can take advantage of this by equiping each nested function with an LRU cache. 
Second, we can speed up the program by paralellizing the computation, since the RGB values of a given pixel can be calculated independently from the others. 
With these optimizations, the computation of the [full image](/original_post.png) took 14 minutes in Python. 
