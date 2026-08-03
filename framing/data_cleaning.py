import pandas as pd
import numpy as np

df1=pd.read_csv("data/raw/online_retail_II_2009.csv")
df2=pd.read_csv("data/raw/online_retail_II_2010.csv")

# print(df1["Customer ID"].isnull().sum()) #107927
# print(df2["Customer ID"].isnull().sum()) #135080
df = pd.concat([df1, df2], ignore_index=True)
df.to_csv("data/raw/online_retail_II_full.csv", index=False)
print("before:", len(df)) # 1067371
df = df.drop_duplicates(keep="last")
print("after:", len(df)) #  1033036
# number of duplicated values per column (excluding the first occurrence)
print(df.duplicated().sum())  # لازم يصير 0
print(df.isnull().sum())  # لازم يصير 0
# drop the nul values 
df = df.dropna(subset=["Customer ID"])