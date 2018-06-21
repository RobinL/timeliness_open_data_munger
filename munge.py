# Purpose:  Convert our open data into Hadley Wickham's tidy data format
import pandas as pd 

df = pd.read_csv("https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/695412/cc-rdos-by-offence-group-q4-2017.csv")
# Delete totals - these should not be present in tidy data
drop = [c for c in df.columns if 'Total' in c]
df = df.drop(drop, axis=1)

# Melt data into tidy format. The open data in in a 'cross tabulation' type format
df.columns = [c.lower() for c in df.columns]
df.columns = [c.replace(" ", "_") for c in df.columns]

id_cols = [c for c in df.columns if '-' not in c]
value_cols = [c for c in df.columns if '-' in c]

df = pd.melt(df,id_vars = id_cols , value_vars = value_cols)


renames = {
    "quarter.1" : "date_range",
    "courttype" : "court_type",
    "lcjb": "local_criminal_justice_board"    
}

df = df.rename(columns=renames)


df["variable"] = df["variable"].str.replace("non-motoring", "non_motoring")
df["yearquarter"] = df["year"].astype(str) + df["quarter"]

df2 = df["variable"].str.split("-", expand=True)
df2.columns = ["variable_type", "offence_type"]

df = df.join(df2)

df["offence_type"] = df["offence_type"].str.replace("_", " ").str.title()
df["variable_type"] = df["variable_type"].str.replace("_", " ").str.title()

cols = [c for c in df.columns if c  not in ["variable_type", "offence_type", "value", "variable"]]
cols.extend(["offence_type", "variable_type", "value"])

df = df[cols]

df["value"] = pd.to_numeric(df["value"], errors='coerce')

ind = ['variable_type']
ind.extend([c for c in df.columns if c not in ('variable_type', 'value')])

df = df.set_index(ind).unstack(level=0).reset_index()
df.columns = [' '.join(col).strip() for col in df.columns.values] 
df.columns = [df.columns.str.replace("value ", "").str.lower()]



df.to_csv("timeliness-transparency-2017Q4.csv" index=False)

