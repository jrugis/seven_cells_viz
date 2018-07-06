# -*- coding: utf-8 -*-
#
# mat2vtk.py

import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.io as sc
import struct
import subprocess
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

##################################################################
# main program
##################################################################

cell_num = 1
mesh_name = '4sim_out_N4_p3-p2-p4-' + str(cell_num) + 'tet.bin'
dist_name = 'Ca_1_7.mat'
dist_key = 'c_all'

print
print 'reading data file: ' + dist_name 
dist = sc.loadmat(dist_name)
#print 'keys:', dist.keys()
node_data = dist[dist_key]
print node_data.shape

print
print 'cell number: ', cell_num
print 'reading binary mesh file: ' + mesh_name
verts = read_bin(mesh_name) 
print verts.shape

c_data = np.transpose(node_data[0, cell_num-1])
print c_data.shape
print 'max =', '{:0.3f}'.format(c_data.max())
print 'min =', '{:0.3f}'.format(c_data.min())
p1 = plt.plot(c_data[:,0:10])
plt.show(p1)

## write vtk time series files
print 'creating vtk time series files...'
if os.path.isdir(str(cell_num)):
  os.system("rm -rf " + str(cell_num))
  os.mkdir(cell_num)
#i_start = 0
#i_finish = node_data.shape[0]
#node_count = node_data.shape[1]
#for i in xrange(i_start, i_finish, 1):
#  d = {}
#  d["c"] = node_data[i, :]
#  d["dnl"] = dnl
#  d["ab"] = ab_data
#  fname = cell_num + '/' + cell_num + '_' + str(i).zfill(4)
#  #print xyz[0,:].shape
# #print dist[:, i].shape   
#  pointsToVTK(fname, xyz[0,:], xyz[1,:], xyz[2,:], data = d)

