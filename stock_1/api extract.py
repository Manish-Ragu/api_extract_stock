import requests
# from io import StringIO
import pandas as pd
pd.set_option('display.max_columns', None)
import csv
github_api_url = "https://api.github.com/repos/squareshift/stock_analysis/contents/"
response = requests.get(github_api_url)
files = response.json()
# print(files)
csv_files = [i['download_url'] for i in files if i['name'].endswith('.csv')]
# print(csv_files)
a=csv_files[0]
# print(a)
csv_file = csv_files.pop()
# print(csv_file)
d = pd.read_csv(csv_file)
# print(d)
# print(d.columns)
# print(d["Sector"])
dataframes=[]
file_names=[]
for j in csv_files:
    file_name = j.split("/")[-1].replace(".csv", "")
    # print(file_name)
    df = pd.read_csv(j)
    df['Symbol'] = file_name
    # print(df['Symbol'])
    dataframes.append(df)
    file_names.append(file_name)
# print(dataframes)
# print(file_names)
combined_df = pd.concat(dataframes, ignore_index=True)
# print(combined_df)
# print(combined_df.columns)
o_df = pd.merge(combined_df,d,on='Symbol',how='left')
# print(o_df)
# print(o_df.columns)
# print(o_df[2:5])
# print(o_df["timestamp"])
result = o_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
# print(result)
o_df["timestamp"] = pd.to_datetime(o_df["timestamp"])
# print(o_df["timestamp"])
# print(o_df.dtypes)
# # to find to no of rows
# print(len(o_df))
# #to find no.of rows and columns
# print(o_df.shape)
# # to find first  row(default = 5 rows will come) - need to give number in bracket of head
# print(o_df.head())
# # to find last 1 row (default = 5 rows will come)
# print(o_df.tail())
filtered_df = o_df[(o_df['timestamp'] >= "2021-01-01") & (o_df['timestamp'] <= "2021-05-26")]
# print(filtered_df)
result_time = filtered_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
list_sector = ["TECHNOLOGY","FINANCE"]
result_time = result_time[result_time["Sector"].isin(list_sector)].reset_index(drop=True)
print(result_time)
path=r"api extract.csv"
result_time.to_csv(path,header=True)
print("data has been written successfully")