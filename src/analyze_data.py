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
