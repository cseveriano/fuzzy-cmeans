import numpy as np
import math
from scipy import io as sio
import matplotlib.pyplot as plt
import Cluster


data = sio.loadmat('fcm_dataset.mat')

#Cluster.c_means(4,data["x"])

Cluster.fuzzy_c_means(4,data["x"],2)