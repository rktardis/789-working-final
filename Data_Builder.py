#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 12:46:35 2023

@author: richard
"""

import pandas as pd
## imports pandas module for later functions

#%% Data read in and quick format

tolls=pd.read_csv("Master_toll_list.csv")
## imports toll data compiled in Final_Data_Compiler.py

mmkr=pd.read_csv("NYS_Thruway_Mile_Markers.csv")
## imports milemarker data

mmkr_n=mmkr[["Ent","Ent_Ref","Ent_Mile"]]

mmkr_x=mmkr[["Exit","Exit_Ref","Exit_Mile"]]

mmkr_2=mmkr.set_index("Ent").drop(labels=["B1","B2","B3","16H"],axis=0).reset_index()

mmkr_n2=mmkr_2[["Ent","Ent_Ref"]]

mmkr_x2=mmkr_2[["Exit","Exit_Ref"]]
## isolates out columns for entrance and exit merges

class_refs=pd.read_csv("class_references.csv")

tolls["Ent"]=tolls["Ent"].astype(str)
## sets data type for entrance number to string

#%% Lists for later

col_order=["Pair","Count","Class","yr","mo","Ent_Mile","Ent","Ent_Ref","Exit_Mile","Exit","Exit_Ref"]

colgroup=["Pair","Class","yr","mo","Ent_Mile","Ent","Ent_Ref","Exit_Mile","Exit","Exit_Ref"]
## list to set order of columns and grouping of columns later

#%% function defining

def ref_merge(v):
    
    v=pd.merge(v,mmkr_x,on="Exit",how="left")
    
    v=pd.merge(v,mmkr_n,on="Ent",how="left")
    
    return v

def exit_cleanup(v):
    
    v=v.drop(columns=["Exit","Ent"])
    
    v=pd.merge(v,mmkr_x2,on="Exit_Ref",how="left")
    
    v=pd.merge(v,mmkr_n2,on="Ent_Ref",how="left")
    
    v=v.query("Ent_Ref!=Exit_Ref")
    ## Replaces any B exits with exit 21A. B exits are exits on the Berkshire spur, a short portion of the thruway connecting from Exit 21A to the Mass border where it becomes the Mass Pike. 
    ## Also replaces 16H coded trips with exit 16, as it is the Harriman toll gantry.

    v=v.query("Ent_Ref<=162 and Exit_Ref<=162")
    ## removes data from dataframe for undesired exits. Exits between 50 and 55 are not tolled and data is not collected. So therefore, analysis is limited to exits east of 50.
    
    return v


## defines function which adds exit reference data via merges
    
def classification (v):
    
    v=v.rename(columns={"Class":"Class_Ref"})
    
    v=pd.merge(v,class_refs,on="Class_Ref",how="left")
    
    v=v.drop(columns="Class_Ref")
    
    ## Assigns simplified class 

    return v

def pairs (v):
    
    rev=v["Exit_Ref"]<v["Ent_Ref"]
    ##creates variable outputting whether or not the exit number is less than the entrance number

    v["Pair"]=v["Ent"]+"-"+v["Exit"]
    ##concatenates each trip from seperate entrance and exit columns into one

    v["Pair"]=v["Pair"].where(rev==False,v["Exit"].astype(str)+"-"+v["Ent"].astype(str))
    ##ensures that trips are in correct order
    
    return v

def all_fnc (v):
    
    v=ref_merge(v)

    v=exit_cleanup(v)
    
    v=classification(v)
    
    v=pairs(v)
    
    v=v.groupby(colgroup).sum().reset_index().loc[:,col_order]
    
    for col in v.columns:
        print(col)
    
    return v

#%% Data Breakout for Processing

tolls_18=tolls.query("Ent<='18'")

tolls_24=tolls.query("'19'<=Ent<='24'")

tolls_30=tolls.query("'25'<=Ent<='30'")

tolls_36=tolls.query("'31'<=Ent<='36'")

tolls_42=tolls.query("'37'<=Ent<='42'")

tolls_48=tolls.query("'43'<=Ent<='48'")

tolls_54=tolls.query("'49'<=Ent<='54'")

tolls_61=tolls.query("'55'<=Ent")
## breaks out toll data into chunks to make data processesing more doable and quicker

#%% performs functions on seperate dataframes

trips_18=all_fnc(tolls_18)

trips_24=all_fnc(tolls_24)

trips_30=all_fnc(tolls_30)

trips_36=all_fnc(tolls_36)

trips_42=all_fnc(tolls_42)

trips_48=all_fnc(tolls_48)

trips_54=all_fnc(tolls_54)

trips_61=all_fnc(tolls_61)
    
#%% Data compilation and save

built=trips_18.append(trips_24,ignore_index=True).append(trips_30,ignore_index=True).append(trips_36,ignore_index=True).append(trips_42,ignore_index=True).append(trips_48,ignore_index=True).append(trips_54,ignore_index=True).append(trips_61,ignore_index=True).sort_values("Pair")

built.to_csv("toll_data_built.csv",index=False)
