#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 15:00:35 2023

@author: richard
"""
import pandas as pd

q1_20=pd.read_csv("NYS_Thruway_Origin_and_Destination_Points_for_All_Vehicles_-_15_Minute_Intervals__2020_Q1.csv")

q2_20=pd.read_csv("NYS_Thruway_Origin_and_Destination_Points_for_All_Vehicles_-_15_Minute_Intervals__2020_Q2.csv")

colname={"Payment Type (Cash or E-Zcom)":"Payment","Entrance":"Ent","Interval Beginning Time":"Time","Vehicle Class":"Class","Vehicle Count":"Count"}

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

journeys=journeys.query("Ent!=37 and Exit!=37 and Ent!='B1' and Exit!='B1' and Ent!='B2' and Exit!='B2' and Ent!='B3' and Exit!='B3'")

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

journeys=journeys.query("Ent!=37 and Exit!=37 and Ent!='B1' and Exit!='B1' and Ent!='B2' and Exit!='B2' and Ent!='B3' and Exit!='B3'")

journeys=q2_20

#%%

comveh=q1_20.query("Class!='2H' and Class!='2L'") 

# =============================================================================
# compymnts=comveh["Payment"].value_counts()
# =============================================================================

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

comtrips_q1_20=comtrips

#%%

comveh=q2_20.query("Class!='2H' and Class!='2L'") 

# =============================================================================
# compymnts=comveh["Payment"].value_counts()
# =============================================================================

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

comtrips_q2_20=comtrips

#%%

diff=comtrips_q2_20-comtrips_q1_20

diff=diff.sort_values("Count")

diff["pct"]=diff["Count"]/comtrips_q1_20["Count"]*100

#%%

com_comp=comtrips_q1_20.drop(columns="pct")

colname4={"Count":"Q1"}

com_comp=com_comp.rename(columns=colname4)

com_comp["Q2"]=comtrips_q2_20["Count"]

# =============================================================================
# com_comp=com_comp.query("Q1>=1000 and Q2>=1000")
# =============================================================================

com_comp["diff"]=com_comp["Q2"]-com_comp["Q1"]

com_comp["diff pct"]=com_comp["diff"]/com_comp["Q1"]*100

com_comp=com_comp.sort_values("diff pct")

#%%

com_comp.to_csv("covid_com_counts.csv")

q1_20.to_csv("com_q1_2020.csv")

q2_20.to_csv("com_q2_2020.csv")