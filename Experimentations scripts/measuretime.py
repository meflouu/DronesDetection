from time import time
import collections
import numpy as np

def onelist(lst):
	for ii in range(int(1E7)):
		lst.append(ii)

def preallocated(lst):
	for ii in range(int(1E7)):
		lst[ii] = ii


# def twolists(lst1, lst2):
# 	for ii in range(int(1E7)):
# 		lst1.append(ii)
# 		lst2.append(ii)

# def list2d(lst):
# 	for ii in range(int(1E7)):
# 		lst.append((ii, ii))

# lst1 = []
# lst2 = []
# t1 = time()
# twolists(lst1, lst2)
# print (time()-t1, len(lst1), len(lst2)) # -> .12

# lst = []
# t2 = time()
# list2d(lst)
# print (time()-t2, len(lst)) # -> .12

pre_allocated_list = [None] * int(1E7)
t3 = time()
preallocated(pre_allocated_list)
print (time()-t3, len(pre_allocated_list)) # -> .12

empty_list = []
t4 = time()
onelist(empty_list)
print (time()-t4, len(empty_list)) # -> .12