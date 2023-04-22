#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:31:11 2023

@author: richard
"""

import requests

import pandas as pd


# =============================================================================
# for_clause="county:*"
# 
# in_clause="state:*"
# 
# payload={"get":"rd33-n4tx", "for":for_clause, "in":in_clause}
# 
# api="https://data.ny.gov/resource/"
# 
# response=requests.get(api,payload)
# 
# row_list=response.json()
# 
# colnames=row_list[0]
# 
# datarows=row_list[1:]
# 
# tolls=pd.DataFrame(columns=colnames, data=datarows)
# 
# =============================================================================

#%%
tolls=pd.read_csv("NYS_Thruway_Origin_and_Destination_Points_for_All_Vehicles_-_15_Minute_Intervals__2020_Q3.csv")

colname={"Payment Type (Cash or E-ZPass)":"Payment","Entrance":"Ent","Interval Beginning Time":"Time","Vehicle Class":"Class","Vehicle Count":"Count"}

tolls=tolls.rename(columns=colname)

#%%
mile_markers=pd.read_csv("NYS_Thruway_Mile_Markers.csv")

journeys=pd.merge(tolls, mile_markers,on="Ent",how="left")

colname2={"Mile":"Ent Mile","Exit_Ref":"Ent_Ref","Exit_x":"Exit"}

journeys=journeys.rename(columns=colname2).drop(columns="Exit_y")

journeys=pd.merge(journeys, mile_markers,on="Exit",how="left")

colname3={"Mile":"Exit Mile","Ent_x":"Ent"}

journeys=journeys.rename(columns=colname3).drop(columns="Ent_y")

journey_int=["Exit_Ref","Ent Mile","Ent_Ref","Exit Mile"]

journeys[journey_int]=journeys[journey_int].astype(float)

journeys["Dist"]=abs(journeys["Exit Mile"]-journeys["Ent Mile"])



#%%
syr_exits=["34A","35","36","37","38","39"]

#%%
samp=tolls.query("Ent=='61' or Exit=='61'")
samp=samp.sort_values("Ent",ascending=False)
# =============================================================================
# print(len(tolls))
# 
# print( "\nColumns:", list(tolls.columns) )
# =============================================================================

# =============================================================================
# pass_class=["2L","2H"]
# =============================================================================

#%%
passveh=tolls.query("Class=='2H' or Class=='2L'") 

passpymnts=passveh["Payment"].value_counts()

rev=passveh["Exit"]<passveh["Ent"]

# =============================================================================
# 
# low=passveh[["Ent","Exit"]].min()
# 
# high=passveh[["Ent","Exit"]].max()
# 
# =============================================================================

passveh["trip"]=passveh["Ent"]+"-"+passveh["Exit"]

passveh["trip"]=passveh["trip"].where(rev==False,passveh["Exit"]+"-"+passveh["Ent"])

passtrips=passveh.groupby("trip").sum()

passtrips=passtrips.drop(columns="Time")

passtrips=passtrips.sort_values("Count")

passtrips["pct"]=100*passtrips["Count"]/passtrips["Count"].sum()

# =============================================================================
# pass_veh=tolls.query("Class"==pass_class)
# =============================================================================
#%%

comveh=tolls.query("Class=='3L' or Class=='4L'or Class=='3H'or Class=='4H'or Class=='5H'or Class=='6H'or Class=='7H'") 

compymnts=comveh["Payment"].value_counts()

rev=comveh["Exit"]<comveh["Ent"]

# =============================================================================
# 
# low=comveh[["Ent","Exit"]].min()
# 
# high=comveh[["Ent","Exit"]].max()
# 
# =============================================================================

comveh["trip"]=comveh["Ent"]+"-"+comveh["Exit"]

comveh["trip"]=comveh["trip"].where(rev==False,comveh["Exit"]+"-"+comveh["Ent"])

comtrips=comveh.groupby("trip").sum()

comtrips=comtrips.drop(columns="Time")

comtrips=comtrips.sort_values("Count")

comtrips["pct"]=100*comtrips["Count"]/comtrips["Count"].sum()