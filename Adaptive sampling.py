import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import time
from shutil import copyfile
os.chdir('F:\\yasara\\yasara\\pym')
from yasara import *
DelObj('All')
os.chdir('F:\\yasara\\mdfa-replica')
CD('F:\\yasara\\mdfa-replica', onstartup=None)
samplename='6gv1_inward'
data=pd.read_excel('MSM.xlsx',index_col=(0))
data=np.array(data.iloc[:,0:2])

'''#clustering
n_clusters=4
cluster = KMeans(n_clusters=n_clusters,random_state=0).fit(data)
centroid=cluster.cluster_centers_'''

'''plt.scatter(data[:,0],data[:,1],s=2)
plt.scatter(centroid[0,0],centroid[0,1],marker='x',color='black',s=100)
plt.scatter(centroid[1,0],centroid[1,1],marker='x',color='black',s=100)
plt.scatter(centroid[2,0],centroid[2,1],marker='x',color='black',s=100)
plt.scatter(centroid[3,0],centroid[3,1],marker='x',color='black',s=100)'''
length= 18830 #length is the current number that has snapshot
a=np.array([0,0])
b=np.array([22,5])
DelObj('All')    
LoadSce(samplename+'_water.sce')
for i in range(len(data),length):  #length is the current snapshot
    if i<10:
        name=samplename+'0000'+str(i)+'.sim'
    elif i<100:
        name=samplename+'000'+str(i)+'.sim'
    elif i<1000:
        name=samplename+'00'+str(i)+'.sim'
    elif i<10000:
        name=samplename+'0'+str(i)+'.sim'
    else:
        name=samplename+str(i)+'.sim'
    LoadSim(name)
    temp_dist=GroupDistance('598-609','5517-5538'),GroupDistance('1923-1937','5017-5040')
    temp_dist=np.array([temp_dist])
    data=np.vstack((data,temp_dist))
DelObj('All')

length=len(data)

def get_snap(length,x):
    dist=[]
    for i in range(length):
        dist.append(np.linalg.norm(data[i] - x))
    return(dist.index(min(dist)))  

def get_name(x):
    if x<10:
        name=samplename+'0000'+str(x)+'.sim'
    elif x<100:
        name=samplename+'000'+str(x)+'.sim'
    elif x<1000:
        name=samplename+'00'+str(x)+'.sim'
    elif x<10000:
        name=samplename+'0'+str(x)+'.sim'
    else:
        name=samplename+str(x)+'.sim'
    return name
    
def new_start(x,y):
    copyfile(get_name(x),get_name(y+1))
    
def play_marco(length,y):# x is the samplename, y is the cycle for next simulation 
    DelObj('All')
    ApplyMacro("F:\yasara\yasara\mcr\md_runmembrane.mcr","6gv1_inward.sce")
    filelist=os.listdir()
    while get_name(length+y) not in filelist:
        time.sleep(300)
        filelist=os.listdir()
    DelObj('All')
    total_dist=np.empty([0,2])
    LoadSce(samplename+'_water.sce')
    for i in range(length,length+y):
        if i<10:
            name=samplename+'0000'+str(i)+'.sim'
        elif i<100:
            name=samplename+'000'+str(i)+'.sim'
        elif i<1000:
            name=samplename+'00'+str(i)+'.sim'
        elif i<10000:
            name=samplename+'0'+str(i)+'.sim'
        else:
            name=samplename+str(i)+'.sim'
        LoadSim(name)
        temp_dist=GroupDistance('598-609','5517-5538'),GroupDistance('1923-1937','5017-5040')
        temp_dist=np.array([temp_dist])
        total_dist=np.vstack((total_dist,temp_dist))
    return total_dist
    DelObj('All')    
        
 
for i in range(5):
    data=np.vstack((data,play_marco(length, 3)))
    length=len(data)
    new_start(get_snap(length,a),length)
    data1=pd.DataFrame(data)
    data1.to_excel('MSM.xlsx')
DelObj('All')  

plt.scatter(data[:,0],data[:,1],s=5,color='red',linewidth=0) 
plt.scatter(data[:18800,0],data[:18800,1],s=5,color='green',linewidth=0)
