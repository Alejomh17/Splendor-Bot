# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 15:32:05 2019

@author: huber.288
"""


from Splendor import *
import numpy as np
from InputVector import *
from MakeMove import *
from NeuralNet4 import *
from NeuralNet2 import Neural_Network2
import torch
import copy
from copy import deepcopy
from NaturalSelection4 import *
import matplotlib.pyplot as plt
from InitializeRandomCards import *
from helper import *
from ReinforcementSelection import ReinforcementSelection

cont=0
step=.3
if not cont:
    AllWeights=[]
    AllLayers=[]
    AvScores=[]

    Nnets=25
    Ngames=10
    MaxTurns=13
    Ngens=50
    Stall=20
    Stallp=.3
    step=1
    mutation=1
    Levels=1
    GameType=1
    lastdrop=0
    NetSize=[46,30,26]
    pReinforce=.5
    Ancestors=list(range(Nnets))

for i3 in range(Ngens):
    Turns=np.zeros((Nnets,Ngames))+MaxTurns+2
    for i0 in range(Nnets):
        if i3==0 and not cont:
            Weights=[]
            pre=Neural_Network2(NetSize,Weights)
            for W in pre.W:
                Weights.append(W.t())
            NN=NeuralNet4(deepcopy(NetSize),Weights)
            AllWeights.append(NN.return_parameters())
            AllLayers.append(deepcopy(NN.LayerSizes))
        else:
            NN=NeuralNet4(WeightSize(AllWeights[i0]),AllWeights[i0])
        for i2 in range(Ngames):
            Game=Splendor(1,GameType)
            for i in range(MaxTurns):
                #IV=InputVector_Simple(Game,46)
                playern=0
                Player=Game.player[0]
                MakeMove(Game,playern,Player,NN,Levels)
                Game.CheckWin()
                if Game.winner:
                    Turns[i0,i2]=i+1# +Game.player[0].VPs/100
                    break
    Scores=np.mean(Turns,axis=1)
    AllWeights,Ps,Ancestors=ReinforcementSelection(AllWeights,Ancestors,Scores,NetSize,step,Nnets,pReinforce,GameType,Levels)
    print([min(Scores),Ps[0],Ps[4]])
    AvScores.append([min(Scores),Ps[0],Ps[4]])
    if i3-lastdrop>Stall:
        if AvScores[-Stall][0]<=AvScores[-1][0] and AvScores[-Stall][1]<=AvScores[-1][1]:  #If fittness has converged, lower step size
            step*=Stallp
            lastdrop=i3
            print(step)
            

plt.plot(AvScores) 
plt.ylabel('Average turns to win')
plt.xlabel('Generation')  
plt.legend(['Best','10th percentile','Median'])

#Levels=0
#Turns=[]
#for i in AllWeights:
#    NN=NeuralNet4(NetSize,i)
    #Turns.append(ThoroughCheck(NN,GameType,Levels))

#Scores=np.mean(Turns,axis=1)
#Ps=[]
#for i in range(9):
    #Ps.append(np.percentile(Scores,(i+1)*10))
#print([min(Scores),Ps[0],Ps[4]])

    
    
