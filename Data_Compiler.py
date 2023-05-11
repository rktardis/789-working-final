#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 10:23:53 2023

@author: richard
"""

import pandas as pd
## imports pandas module for later functions

tolls_15=pd.read_csv("NYS_Thruway_Origin_and_Destination_Points_for_All_Vehicles_-_1_Hour_Intervals__2015.csv")

tolls_16=pd.read_csv("NYS_Thruway_Origin_and_Destination_Points_for_All_Vehicles_-_1_Hour_Intervals__2016.csv")

tolls_17=pd.read_csv("NYS_Thruway_Origin_and_Destination_Points_for_All_Vehicles_-_1_Hour_Intervals__2017.csv")

tolls_18=pd.read_csv("NYS_Thruway_Origin_and_Destination_Points_for_All_Vehicles_-_1_Hour_Intervals__2018.csv")

tolls_19=pd.read_csv("NYS_Thruway_Origin_and_Destination_Points_for_All_Vehicles_-_1_Hour_Intervals__2019.csv")

tolls_20=pd.read_csv("NYS_Thruway_Origin_and_Destination_Points_for_All_Vehicles_-_1_Hour_Intervals__2020.csv")
##reads in data downloaded from state

#%%

colname={"Payment Type":"Payment","Entrance":"Ent","Interval Beginning Time":"Time","Vehicle Class":"Class","Vehicle Count":"Count"}
## creates dictionaries for column renaming

coldate=["mo","d","yr"]
## creates list of column names for later date splitting

colfloat=["Count","mo","yr"]
## date columns for split and type change

#%%

def intake (var):
    var=var.rename(columns=colname).groupby(["Date","Ent","Exit","Class","Count"]).sum().reset_index().drop(columns="Time")
    ## renames columns, groups and sums by required variables

    var[coldate]=var.Date.str.split("/",expand=True)
    ## splits date variable into individual variables for day, month, year

    var=var.groupby(["Date","Ent","Exit","Class","Count","mo","yr"]).sum().reset_index().drop(columns=["d","Date"])
    ## renames columns, groups and sums by required variables
    
    var[colfloat]=var[colfloat].astype(float)
    ## sets certain columns to float for later calculations
    
    return var

#%%

tolls_15=intake(tolls_15)

tolls_16=intake(tolls_16)

tolls_17=intake(tolls_17)

tolls_18=intake(tolls_18)

tolls_19=intake(tolls_19)

tolls_20=intake(tolls_20)
## performs function on each year of data

#%%

trips=tolls_17.append(tolls_18,ignore_index=True).append(tolls_19,ignore_index=True).append(tolls_20,ignore_index=True).append(tolls_15,ignore_index=True).append(tolls_16,ignore_index=True)
## compiles all formatted year data into one dataframe

#%% Data Saving

trips.to_csv("Master_toll_list.csv", index=False)
## saves dataframe with all formatted data