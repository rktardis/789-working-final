#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 15:16:45 2023

@author: richard
"""

import pandas as pd

counts=pd.read_csv("covid_pass_counts.csv")

mile_markers=pd.read_csv("NYS_Thruway_Mile_Markers.csv")
##imports thruway trip data and thruway exit milemarker data

counts[["Ent","Exit"]]=counts.trip.str.split("-",expand=True)
##splits trip column into entrance and exit columns (e.g. a trip between exit 28 and 34A goes from "28-34A" to two seperate columns, "28" and "34A")



journeys=pd.merge(counts, mile_markers,on="Ent",how="left")
##uses milemarker data to assign entrance milemarker

colname2={"Mile":"Ent Mile","Exit_Ref":"Ent_Ref","Exit_x":"Exit"}

journeys=journeys.rename(columns=colname2).drop(columns="Exit_y")
##drops unnecessary columns and renames others

journeys=pd.merge(journeys, mile_markers,on="Exit",how="left")
##uses milemarker data to assign exit milemarker

colname3={"Mile":"Exit Mile","Ent_x":"Ent"}

journeys=journeys.rename(columns=colname3).drop(columns="Ent_y").drop(columns="diff pct")
##drops unnecessary columns and renames others

journeys=journeys.query("Ent!='16H' and Exit!='16H' and Ent!=37 and Exit!=37 and Ent!='B1' and Exit!='B1' and Ent!='B2' and Exit!='B2' and Ent!='B3' and Exit!='B3'")
##drops trips for exit 37 as it was closed for part of 2020 and other exits for not having milemarker data at present

journey_int=["Exit_Ref","Ent Mile","Ent_Ref","Exit Mile"]

journeys[journey_int]=journeys[journey_int].astype(float)
#makes new columns into floats

journeys["Dist"]=abs(journeys["Exit Mile"]-journeys["Ent Mile"])
#calculates distance traveled

counts=journeys

# =============================================================================
# col_drop=["Exit","Ent","Exit Mile","Ent Mile","Exit_Ref","Ent_Ref"]
# 
# test=test.drop(columns=col_drop)
# =============================================================================
