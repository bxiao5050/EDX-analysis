from tkinter import *
import numpy as np

a = np.array([[1,i] for i in range(1,5)])
n = 5
corners =np.array([(np.sin(2*np.pi/i), np.cos(2*np.pi/i), 0 )for i in range(1, n)])
print(corners)
