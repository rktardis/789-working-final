#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 11:37:18 2023

@author: richard
"""

import pandas as pd
# =============================================================================
# import seaborn as sns
# import matplotlib.pyplot as plt
# =============================================================================

drpcol=["yr","mo"]

drpcol2=["Pair","Ent_Ref","Count"]

drpcol3=["Exit_x","Ent_y","Ent_Ref","Exit_Ref"]

rnmcol={"Exit_y":"Exit","Ent_x":"Entrance"}

colgroup=["Pair","Ent","Ent_Ref","Exit","Exit_Ref"]

## lists or dictionaries of columns to drop or rename later

colref=["Ent_Ref","Exit_Ref"]

colref2=["Ent_Mile","Exit_Mile"]

colcref=["C_Ent_Ref","C_Exit_Ref"]

exits=list(range(76))[20:]
## lists of exit reference numbers

seg_count={"Exit":"Count"}
##start dictionary for later

#%% Data imports and organization

trips=pd.read_csv("toll_data_built.csv")

trips[colref2]=trips[colref2].astype(str)

trips["Count"]=trips["Count"].astype(int)
## reads in previously compiled data

#%% Exit columns organization

rev=trips["Exit_Ref"]<trips["Ent_Ref"]

trips["C_Exit_Ref"]=trips["Ent_Ref"].where(rev==True,trips["Exit_Ref"])

trips["C_Ent_Ref"]=trips["Exit_Ref"].where(rev==True,trips["Ent_Ref"])

trips["Ent_Ref"]=trips["C_Ent_Ref"].astype(int)

trips["Exit_Ref"]=trips["C_Exit_Ref"].astype(int)

trips=trips.drop(columns=colcref)

trips[["Ent","Exit"]]=trips.Pair.str.split("-",expand=True)

#%% math

trips=trips.groupby(colgroup).sum().reset_index().drop(columns=drpcol).sort_values("Count",ascending=False)
## groups and sums trip data by pair, drops irrelevant columns, and sorts by count

#%% Data Save

trips.to_csv("Thruway_Pair_Data.csv",index=False)
