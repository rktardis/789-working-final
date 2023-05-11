#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 15:43:52 2023

@author: richard
"""
import pandas as pd

#%% Data reading
trips=pd.read_csv("toll_data_built.csv")

#%% lists etc.

exdropcol=["Ent Mile","Exit Mile","Time","month","day"]

veh_pass="Class=='2H' or Class=='2L'"

veh_com="Class=='3L' or Class=='4L'or Class=='3H'or Class=='4H'or Class=='5H'or Class=='6H'or Class=='7H'"

#%% Counts
exits=trips.groupby("Exit").sum().drop(columns=exdropcol).sort_values("Count",ascending=False)

ents=trips.groupby("Ent").sum().drop(columns=exdropcol).sort_values("Count",ascending=False)

ents["Exit"]=ents.index

idv_counts=pd.merge(exits,ents,on="Exit",how="left").rename(columns={"Exit":"Number","Count_x":"Exit Count","Count_y":"Ent Count"}).set_index("Number").loc[:,["Ent Count","Exit Count"]]

idv_counts["Total"]=idv_counts["Exit Count"]+idv_counts["Ent Count"]

idv_counts["Ent %"]=idv_counts["Ent Count"]/idv_counts["Total"]

idv_counts_all=idv_counts.sort_values("Ent %").rename(columns={"Ent Count":"Ent Total","Exit Count":"Exit Total","Total":"Grand Total","Ent %":"All Ent %"})

#%% com trips

com_trips=trips.query(veh_com)

exits=com_trips.groupby("Exit").sum().drop(columns=exdropcol).sort_values("Count",ascending=False)

ents=com_trips.groupby("Ent").sum().drop(columns=exdropcol).sort_values("Count",ascending=False)

ents["Exit"]=ents.index

idv_counts=pd.merge(exits,ents,on="Exit",how="left").rename(columns={"Exit":"Number","Count_x":"Exit Count","Count_y":"Ent Count"}).set_index("Number").loc[:,["Ent Count","Exit Count"]]

idv_counts["Total"]=idv_counts["Exit Count"]+idv_counts["Ent Count"]

idv_counts["Ent %"]=idv_counts["Ent Count"]/idv_counts["Total"]

idv_counts_com=idv_counts.sort_values("Ent %").rename(columns={"Ent Count":"Ent Com","Exit Count":"Exit Com","Total":"Com Total","Ent %":"Com Ent %"})

#%% pass trips

pass_trips=trips.query(veh_pass)

exits=pass_trips.groupby("Exit").sum().drop(columns=exdropcol).sort_values("Count",ascending=False)

ents=pass_trips.groupby("Ent").sum().drop(columns=exdropcol).sort_values("Count",ascending=False)

ents["Exit"]=ents.index

idv_counts=pd.merge(exits,ents,on="Exit",how="left").rename(columns={"Exit":"Number","Count_x":"Exit Count","Count_y":"Ent Count"}).set_index("Number").loc[:,["Ent Count","Exit Count"]]

idv_counts["Total"]=idv_counts["Exit Count"]+idv_counts["Ent Count"]

idv_counts["Ent %"]=idv_counts["Ent Count"]/idv_counts["Total"]

idv_counts_pass=idv_counts.sort_values("Ent %").rename(columns={"Ent Count":"Ent Pass","Exit Count":"Exit Pass","Total":"Pass Total","Ent %":"Pass Ent %"})

#%% 

idv_counts=pd.merge(idv_counts_pass,idv_counts_com,on="Number",how="left")

idv_counts=pd.merge(idv_counts,idv_counts_all,on="Number",how="left")

idv_counts["Pass %"]=idv_counts["Pass Total"]/idv_counts["Grand Total"]

idv_counts=idv_counts.sort_values("Pass %")

#%% Export

idv_counts.to_csv("Individual Exit Counts.csv")
