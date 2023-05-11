#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 11:56:20 2023

@author: richard
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 300

#%% 

trips=pd.read_csv("toll_data_built.csv")
## reads in data

coldrp=["Pair","Ent_Mile","Exit_Mile","Ent","Exit","Exit_Ref","Ent_Ref","yr","mo"]

colgrp=["Class","Time"]

classes=["Commercial","Passenger"]
## creates lists for later

#%%

trips["Time"]=trips["yr"]+(trips["mo"]-1)/12
## creates single time column

trips=trips.drop(columns=coldrp).groupby(colgrp).sum().reset_index()
## drops unnecesary columns and groups by others

comtrips=trips.query("Class=='Commercial'").rename(columns={"Count":"Commercial"}).drop(columns="Class")

passtrips=trips.query("Class=='Passenger'").rename(columns={"Count":"Passenger"}).drop(columns="Class")

trips=pd.merge(passtrips,comtrips,on="Time",how="left")
##seperates counts for commercial and passenger vehicles

trips[classes]=trips[classes]/1e6
## converts counts to millions

trips=trips.query("Time<=2020.7")
## removes data from portions of 2020 with incomplete data

trips=trips.set_index("Time")

fig1=trips[["Passenger","Commercial"]].plot.line()

plt.title("NYS Thruway Passenger and Commercial Use")

fig1.figure.savefig("Usage_Over_Time_by_Type.png")

trips["com_prp"]=trips["Commercial"]/max(trips["Commercial"])

trips["pass_prp"]=trips["Passenger"]/max(trips["Passenger"])
## creates columns with a proportion of trips relative to the maximum, to illustrate how passenger and commercial trips change differently

fig2=trips[["pass_prp","com_prp"]].plot.line()

plt.title("NYS Thruway Passenger and Commercial Relative Use")

fig2.figure.savefig("Relative_Usage_Over_Time_by_Type.png")
## creates and saves graph

trips.to_csv("rel_use_time_class.csv")