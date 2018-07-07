# -*- coding: utf-8 -*-
#
# mat2vtk.py

import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.io as sc
import struct
import subprocess
import time
from evtk.hl import pointsToVTK

#import cs

##################################################################
# functions
##################################################################

def read_bin(fname):
  f1 = open(fname, 'rb') # open the binary file
  # get the vertices
  nverts = struct.unpack('i', f1.read(4))[0]
  verts = np.empty([nverts, 3])
  for i in range(nverts):
    verts[i] = struct.unpack('fff', f1.read(12))
  f1.close # close the binary file 
  return verts

###########################################################################
def write_points(fname, verts, d):
  nverts = verts.shape[0]
  xyz = np.empty([3, nverts]) # needs re-ordering
  for i in range(nverts):
    for j in range(3):
      xyz[j,i] = verts[i,j]  
  pointsToVTK(fname, \
    xyz[0,:], xyz[1,:], xyz[2,:], \
    data=d)  # write out vtu file
  return

##################################################################
# main program
##################################################################

dist_name = 'Ca_1_7.mat'
dist_key = 'c_all'

start_time = time.time()
print
print 'reading data file: ' + dist_name 
dist = sc.loadmat(dist_name)
#print 'keys:', dist.keys()
node_data = dist[dist_key]
print node_data.shape

for cell_num in range(1,8):
  print
  print 'cell number: ', cell_num
  mesh_name = '4sim_out_N4_p3-p2-p4-' + str(cell_num) + 'tet.bin'
  print 'reading binary mesh file: ' + mesh_name
  verts = read_bin(mesh_name)
  print verts.shape

  c_data = np.transpose(node_data[0, cell_num-1])
  print c_data.shape
  print 'max =', '{:0.3f}'.format(c_data.max())
  print 'min =', '{:0.3f}'.format(c_data.min())
#  plt.plot(c_data[:,0:10])
#  plt.show()

  ## write vtk time series files
  print 'creating vtk time series files'
  if os.path.isdir(str(cell_num)):
    os.system("rm -rf " + str(cell_num))
  os.mkdir(str(cell_num))
  i_start = 0
  i_finish = c_data.shape[0]
  #i_start = 500
  #i_finish = 800

  c_count = c_data.shape[1]
  for i in range(i_start, i_finish, 1):
    d = {}
    d["c"] = c_data[i,:]
    fname = str(cell_num) + '/' + str(cell_num) + '_' + str(i).zfill(4)
    write_points(fname, verts, d)

print 'elapsed time: ', time.time - start_time, ' s'

