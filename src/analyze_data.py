import pandas as pd

df = pd.read_csv('data/laboratory_results.csv')

print("\n First rows:")
print(df.head())

print("\n Dataset dimensions:")
print(df.shape)

print("\n Column names:")
print(df.columns)

print("\n Data types:")
print(df.dtypes)

print("\n Structural info:")
df.info()

print("\n Statistical summary:")
print(df.describe())

print("\nData validation:")

print("\nCount null values:")
print(df.isna().sum())

print("\nCount duplicate rows:")
print(df.duplicated().sum())

print("\nVerify if there is duplicate IDs:")
print(df["Sample_ID"].duplicated().sum())

print("\nShow the unique values of Sample type, Test, Unit and Analyzer:")
print("Sample type:", df["Sample_Type"].unique())
print("Test:", df["Test"].unique())
print("Unit:", df["Unit"].unique())
print("Analyzer:", df["Analyzer"].unique())

print("\nData type check:")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
print(df["Date"].dtype)

print("\n Count invalid date: ")
print(df["Date"].isna().sum())


