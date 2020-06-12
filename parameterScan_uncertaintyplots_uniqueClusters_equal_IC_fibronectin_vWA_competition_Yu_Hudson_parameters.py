# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 10:22:08 2020

@author: Zeynep Karagoz

# -*- coding: utf-8 -*-
"""

#Importing relevant packages
import tellurium as te # Python-based modeling environment for kinetic models
import roadrunner as rr # High-performance simulation and analysis library
import numpy as np # Scientific computing package
import matplotlib.pylab as plt # Additional Python plotting utilities
import pandas as pd
import os
import seaborn as sns
import math
os.chdir(r'C:\karagoz\01-RESEARCH\01-Projects\01-In_silico_modeling_of_Integrin_function\003-Ligand_competition_model\Unique_clusters\figures_FN_vWF_equal_IC')



#%% 
# 2 ligand 1 integrin  

# setting the ligands to EQUAL initial conditions
# differentiating between 3 types of clusters IF+IF, IW+IW and IF+IW 
# but the rates of clustering are the same between 3 clusters. only the identities are different


# ligands: fibronectin and von Willebrand Factor A (initial values adapted from kidney orgaoid iBAQ values)
# integrin avB3 (initial value from Hudson et al)
# here the rate for ligand binding-unbinding  is from Hudson et al (both ligands) 
# activation/inactivation is from  Yu et al. 2017
# clustering forward is numerically from Hudson, then reverse is estimated using the Kd from Yu et al .
Ant_str = """
  model test # activation model 

  species i, I, $F, IF, $W, IW, C1, C2, C3; 
  #inactive integrin, active integrin, fibronectin, integrin+fibronectin, vonWillebrand Factor A, integrin+vonWillebrand Factor A, clustered integrins respectively.
  
  #set initial values:
  i = 0.05; # integrin avB3 
  I = 0; 
  F = 0.33   ; #fibronectin (set the same as vWA)
  IF = 0;
  W = 0.33   ; #von Willebrand factor A 
  IW = 0;  
  C1 = 0;     # IF+IF cluster
  C2 = 0;     # IW + IW cluster
  C3 = 0;     # IF+IW cluster

  J1: i -> I; k1*i - k2*I; # reaction; reaction rate law;   # activation step, k1 rate of activation, k2 rate of inactivation
  J2: I + $F -> IF; k3*I*F - k4*IF;                          # ligand binding step, k3 rate of fibronectin binding, k4 rate of dissociation
  J3: I + $W -> IW; k5*I*W - k6*IW;                          # alternative ligand binding step, k5 rate of vWFA binding, k6 rate of dissociation
  J4: IF + IF -> C1; k7*IF^2 - k8*C1;
  J5: IW + IW -> C2; k7*IW^2 - k8*C2;
  J6: IF + IW -> C3; k7*IF*IW - k8*C3;                         # clustering step, k7 rate of clustering, k8 rate of dissociation

  k1 = 5*10^6; k2 = 10^8; k3 = 1.6*10^8 ; k4 = 3.5*10^-1; k5 = 1.6*10^4 ; k6 = 2.3*10^-2; k7 = 1.6*10^8; k8 = 0.5*10^7; # assign constant values to global parameters
  end
  """
r2 = te.loada(Ant_str)

#k1 = 5*10^6; k2 = 10^8; k3 = 1.6*10^8; k4 = 3.5*10^-1; k5 = 1.6*10^8; k6 = 0.5*10^7; #rates of the ABC model adjusted for 60%clustering

#te.getODEsFromModel(r2)
#vJ1 = k1*i-k2*I
#vJ2 = k3*I*F-k4*IF
#vJ3 = k5*I*W-k6*IW
#vJ4 = k7*pow(IF,2)-k8*C1
#vJ5 = k7*pow(IW,2)-k8*C2
#vJ6 = k7*IF*IW-k8*C3

#di/dt = -vJ1
#dI/dt = vJ1 - vJ2 - vJ3
#dIF/dt = vJ2 - 2.0*vJ4 - vJ6
#dIW/dt = vJ3 - 2.0*vJ5 - vJ6
#dC1/dt = vJ4
#dC2/dt = vJ5
#dC3/dt = vJ6

#%%
def plot_param_uncertainty(model, startVal, name, num_sims):
    stdDev = 0.6
# assumes initial parameter estimate as mean and iterates 60% above and below.
    vals = np.linspace((1-stdDev)*startVal, (1+stdDev)*startVal, 100)
    for val in vals:
        r2.resetToOrigin()
        exec("r2.%s = %f" % (name, val))
        result = r2.simulate(0, 0.00001 , 100 , ['time', 'i', 'I', 'IF', 'IW', 'C1', 'C2', 'C3'])
        plt.plot(result[:,0],result[:,1])
        plt.xticks(rotation=45)
        plt.title("uncertainty in " + name)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Concentration (uM)")
startVals = r2.getGlobalParameterValues();
names = list(enumerate([x for x in r2.getGlobalParameterIds() if ("K" in x or "k" in x)]));
n = len(names) + 1;
dim = math.ceil(math.sqrt(n))

for i,next_param in enumerate(names):
    plt.subplot(dim,dim,i+1)
    plot_param_uncertainty(r2, startVals[next_param[0]], next_param[1], 100)

plt.suptitle('Inactive integrin concentration')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
#plt.show()
plt.savefig('uncertainty_inactiveIntegrin.png')

#%%
r2 = te.loada(Ant_str)
def plot_param_uncertainty(model, startVal, name, num_sims):
    stdDev = 0.6
# assumes initial parameter estimate as mean and iterates 60% above and below.
    vals = np.linspace((1-stdDev)*startVal, (1+stdDev)*startVal, 100)
    for val in vals:
        r2.resetToOrigin()
        exec("r2.%s = %f" % (name, val))
        result = r2.simulate(0, 0.00001 , 100 , ['time', 'i', 'I', 'IF', 'IW', 'C1', 'C2', 'C3'])
        plt.plot(result[:,0],result[:,2])
        plt.xticks(rotation=45)
        plt.title("uncertainty in " + name)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Concentration (uM)")
startVals = r2.getGlobalParameterValues();
names = list(enumerate([x for x in r2.getGlobalParameterIds() if ("K" in x or "k" in x)]));
n = len(names) + 1;
dim = math.ceil(math.sqrt(n))

for i,next_param in enumerate(names):
    plt.subplot(dim,dim,i+1)
    plot_param_uncertainty(r2, startVals[next_param[0]], next_param[1], 100)

plt.suptitle('Active integrin concentration')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
#plt.show()
plt.savefig('uncertainty_activeIntegrin.png')

#%%
r2 = te.loada(Ant_str)
def plot_param_uncertainty(model, startVal, name, num_sims):
    stdDev = 0.6
# assumes initial parameter estimate as mean and iterates 60% above and below.
    vals = np.linspace((1-stdDev)*startVal, (1+stdDev)*startVal, 100)
    for val in vals:
        r2.resetToOrigin()
        exec("r2.%s = %f" % (name, val))
        result = r2.simulate(0, 0.00001 , 100 , ['time', 'i', 'I', 'IF', 'IW', 'C1', 'C2', 'C3'])
        plt.plot(result[:,0],result[:,3])
        plt.xticks(rotation=45)
        plt.title("uncertainty in " + name)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Concentration (uM)")
startVals = r2.getGlobalParameterValues();
names = list(enumerate([x for x in r2.getGlobalParameterIds() if ("K" in x or "k" in x)]));
n = len(names) + 1;
dim = math.ceil(math.sqrt(n))

for i,next_param in enumerate(names):
    plt.subplot(dim,dim,i+1)
    plot_param_uncertainty(r2, startVals[next_param[0]], next_param[1], 100)

plt.suptitle('Fibronectin bound integrin concentration')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
#plt.show()
plt.savefig('uncertainty_FboundIntegrin.png')

#%%
r2 = te.loada(Ant_str)
def plot_param_uncertainty(model, startVal, name, num_sims):
    stdDev = 0.6
# assumes initial parameter estimate as mean and iterates 60% above and below.
    vals = np.linspace((1-stdDev)*startVal, (1+stdDev)*startVal, 100)
    for val in vals:
        r2.resetToOrigin()
        exec("r2.%s = %f" % (name, val))
        result = r2.simulate(0, 0.00001 , 100 , ['time', 'i', 'I', 'IF', 'IW', 'C1', 'C2', 'C3'])
        plt.plot(result[:,0],result[:,4])
        plt.xticks(rotation=45)
        plt.title("uncertainty in " + name)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Concentration (uM)")
startVals = r2.getGlobalParameterValues();
names = list(enumerate([x for x in r2.getGlobalParameterIds() if ("K" in x or "k" in x)]));
n = len(names) + 1;
dim = math.ceil(math.sqrt(n))

for i,next_param in enumerate(names):
    plt.subplot(dim,dim,i+1)
    plot_param_uncertainty(r2, startVals[next_param[0]], next_param[1], 100)

plt.suptitle('vWA bound integrin concentration')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
#plt.show()
plt.savefig('uncertainty_WboundIntegrin.png')

#%%
r2 = te.loada(Ant_str)
def plot_param_uncertainty(model, startVal, name, num_sims):
    stdDev = 0.6
# assumes initial parameter estimate as mean and iterates 60% above and below.
    vals = np.linspace((1-stdDev)*startVal, (1+stdDev)*startVal, 100)
    for val in vals:
        r2.resetToOrigin()
        exec("r2.%s = %f" % (name, val))
        result = r2.simulate(0, 0.00001 , 100 , ['time', 'i', 'I', 'IF', 'IW', 'C1', 'C2', 'C3'])
        plt.plot(result[:,0],result[:,5])
        plt.xticks(rotation=45)
        plt.title("uncertainty in " + name)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Concentration (uM)")
startVals = r2.getGlobalParameterValues();
names = list(enumerate([x for x in r2.getGlobalParameterIds() if ("K" in x or "k" in x)]));
n = len(names) + 1;
dim = math.ceil(math.sqrt(n))

for i,next_param in enumerate(names):
    plt.subplot(dim,dim,i+1)
    plot_param_uncertainty(r2, startVals[next_param[0]], next_param[1], 100)

plt.suptitle('Cluster of fibronectin bound integrin concentration')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
#plt.show()
plt.savefig('uncertainty_C1Integrin.png')
#%%
r2 = te.loada(Ant_str)
def plot_param_uncertainty(model, startVal, name, num_sims):
    stdDev = 0.6
# assumes initial parameter estimate as mean and iterates 60% above and below.
    vals = np.linspace((1-stdDev)*startVal, (1+stdDev)*startVal, 100)
    for val in vals:
        r2.resetToOrigin()
        exec("r2.%s = %f" % (name, val))
        result = r2.simulate(0, 0.00001 , 100 , ['time', 'i', 'I', 'IF', 'IW', 'C1', 'C2', 'C3'])
        plt.plot(result[:,0],result[:,6])
        plt.xticks(rotation=45)
        plt.title("uncertainty in " + name)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Concentration (uM)")
startVals = r2.getGlobalParameterValues();
names = list(enumerate([x for x in r2.getGlobalParameterIds() if ("K" in x or "k" in x)]));
n = len(names) + 1;
dim = math.ceil(math.sqrt(n))

for i,next_param in enumerate(names):
    plt.subplot(dim,dim,i+1)
    plot_param_uncertainty(r2, startVals[next_param[0]], next_param[1], 100)

plt.suptitle('Cluster of vWA bound integrin concentration')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
#plt.show()
plt.savefig('uncertainty_C2Integrin.png')
#%%
r2 = te.loada(Ant_str)
def plot_param_uncertainty(model, startVal, name, num_sims):
    stdDev = 0.6
# assumes initial parameter estimate as mean and iterates 60% above and below.
    vals = np.linspace((1-stdDev)*startVal, (1+stdDev)*startVal, 100)
    for val in vals:
        r2.resetToOrigin()
        exec("r2.%s = %f" % (name, val))
        result = r2.simulate(0, 0.00001 , 100 , ['time', 'i', 'I', 'IF', 'IW', 'C1', 'C2', 'C3'])
        plt.plot(result[:,0],result[:,7])
        plt.xticks(rotation=45)
        plt.title("uncertainty in " + name)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Concentration (uM)")
startVals = r2.getGlobalParameterValues();
names = list(enumerate([x for x in r2.getGlobalParameterIds() if ("K" in x or "k" in x)]));
n = len(names) + 1;
dim = math.ceil(math.sqrt(n))

for i,next_param in enumerate(names):
    plt.subplot(dim,dim,i+1)
    plot_param_uncertainty(r2, startVals[next_param[0]], next_param[1], 100)

plt.suptitle('Cluster of mixed ligand bound integrin concentration')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
#plt.show()
plt.savefig('uncertainty_C3Integrin.png')