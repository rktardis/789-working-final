#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 13:57:53 2023

@author: richard
"""
import pandas as pd

q1_20=pd.read_csv("NYS_Thruway_Origin_and_Destination_Points_for_All_Vehicles_-_15_Minute_Intervals__2020_Q1.csv")

q2_20=pd.read_csv("NYS_Thruway_Origin_and_Destination_Points_for_All_Vehicles_-_15_Minute_Intervals__2020_Q2.csv")

colname={"Payment Type (Cash or E-ZPass)":"Payment","Entrance":"Ent","Interval Beginning Time":"Time","Vehicle Class":"Class","Vehicle Count":"Count"}

q1_20=q1_20.rename(columns=colname)

q2_20=q2_20.rename(columns=colname)

#%%
mile_markers=pd.read_csv("NYS_Thruway_Mile_Markers.csv")

journeys=pd.merge(q1_20, mile_markers,on="Ent",how="left")

colname2={"Mile":"Ent Mile","Exit_Ref":"Ent_Ref","Exit_x":"Exit"}

journeys=journeys.rename(columns=colname2).drop(columns="Exit_y")

journeys=pd.merge(journeys, mile_markers,on="Exit",how="left")

colname3={"Mile":"Exit Mile","Ent_x":"Ent"}

journeys=journeys.rename(columns=colname3).drop(columns="Ent_y")

journey_int=["Exit_Ref","Ent Mile","Ent_Ref","Exit Mile"]

journeys[journey_int]=journeys[journey_int].astype(float)

journeys["Dist"]=abs(journeys["Exit Mile"]-journeys["Ent Mile"])

journeys=q1_20

#%%
mile_markers=pd.read_csv("NYS_Thruway_Mile_Markers.csv")

journeys=pd.merge(q2_20, mile_markers,on="Ent",how="left")

colname2={"Mile":"Ent Mile","Exit_Ref":"Ent_Ref","Exit_x":"Exit"}

journeys=journeys.rename(columns=colname2).drop(columns="Exit_y")

journeys=pd.merge(journeys, mile_markers,on="Exit",how="left")

colname3={"Mile":"Exit Mile","Ent_x":"Ent"}

journeys=journeys.rename(columns=colname3).drop(columns="Ent_y")

journey_int=["Exit_Ref","Ent Mile","Ent_Ref","Exit Mile"]

journeys[journey_int]=journeys[journey_int].astype(float)

journeys["Dist"]=abs(journeys["Exit Mile"]-journeys["Ent Mile"])

journeys=q2_20

#%%

passveh=q1_20.query("Class=='2H' or Class=='2L'") 

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

passtrips_q1_20=passtrips

#%%

passveh=q2_20.query("Class=='2H' or Class=='2L'") 

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

passtrips_q2_20=passtrips

#%%

diff=passtrips_q2_20-passtrips_q1_20

diff=diff.sort_values("Count")

diff["pct"]=diff["Count"]/passtrips_q1_20["Count"]*100

#%%

pass_comp=passtrips_q1_20.drop(columns="pct")

colname4={"Count":"Q1"}

pass_comp=pass_comp.rename(columns=colname4)

pass_comp["Q2"]=passtrips_q2_20["Count"]

# =============================================================================
# pass_comp=pass_comp.query("Q1>=1000 and Q2>=1000")
# =============================================================================

pass_comp["diff"]=pass_comp["Q2"]-pass_comp["Q1"]

pass_comp["diff pct"]=pass_comp["diff"]/pass_comp["Q1"]*100

pass_comp=pass_comp.sort_values("diff pct")

pass_comp.to_csv("covid_pass_counts.csv")