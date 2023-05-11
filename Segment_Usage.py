#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 15:41:28 2023

@author: richard
"""


import pandas as pd
import matplotlib.pyplot as plt

drpcol=["Unnamed: 0","yr","mo"]

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

trips=pd.read_csv("Thruway_Pair_Data.csv")

mmkr=pd.read_csv("NYS_Thruway_Mile_Markers.csv")

mmkr_r=mmkr[["Ent","Exit","Exit_Ref"]]
##reads in milemarker and exit

trips[colref]=trips[colref].astype(int)

trips=trips.sort_values("Count",ascending=False)

trips_Ref=trips[["Ent_Ref","Exit_Ref","Count"]]

#%%

min_ent=trips["Ent_Ref"].min()

max_exit=trips["Exit_Ref"].max()

seg_count={h:0 for h in range(min_ent,max_exit)}

for pair in trips.itertuples():
    s=pair.Ent_Ref
    e=pair.Exit_Ref
    v=pair.Count
    hits=range(s,e)
    print("\n", s, e, v, list(hits))
    for h in hits:
        seg_count[h]+=v

#%%
segs=pd.DataFrame.from_dict(seg_count,orient="index").reset_index()
## turns dictionary with segment count data into dataframe

segs=segs.rename(columns={"index":"Exit_Ref",0:"Trips (M)"})
## drops {"Exit":"Count"} row and renames column

segs=segs.astype(int)

segs=pd.merge(segs,mmkr_r,on="Exit_Ref",how="left")

pairs=segs.copy(deep=True).drop(columns="Exit")

segs=segs.sort_values("Exit_Ref").drop(columns=["Exit_Ref","Ent"]).set_index("Exit")

segs["Trips (M)"]=segs["Trips (M)"]/1e6
##drops irrelevant columns, and renames others to match convention

plt.rcParams["figure.dpi"] = 300

fig1=segs.plot.bar()

plt.title("NYS Thruway Individual Segment Usage")

plt.xticks(fontsize=8, rotation=90)

fig1.figure.savefig("Segment_Usage.png")


#%%

pairs=pairs.rename(columns={"Exit":"Ent","Exit_Ref":"Ent_Ref"})

pairs["Exit_Ref"]=pairs["Ent_Ref"]+1

pairs=pd.merge(pairs,mmkr[["Exit_Ref","Exit"]],on="Exit_Ref",how="left")

pairs["Trips (M)"]=pairs["Trips (M)"]/1e6

pairs["Pair"]=pairs["Ent"]+"-"+pairs["Exit"]

pairs=pairs[["Pair","Trips (M)"]].sort_values("Trips (M)",ascending=False)
            
pairs.to_csv("segment_data.csv",index=False)